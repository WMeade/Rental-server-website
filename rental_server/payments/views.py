from django.shortcuts import render, redirect
from .cart import Cart
from servers.models import unrented_server, rented_server
from .models import payment_details
from other_scripts.generators import id_gens
from cryptography.fernet import Fernet
import stripe
from rentals.models import rental, transaction
import datetime
from rental_Server import settings
import datetime
from decimal import Decimal
from other_scripts.emailing import Outbound
from django.contrib import messages

def add_cart(request, server_id):
    cart = Cart(request)
    server = unrented_server.objects.get(id=server_id)
    cart.add(server=server)
    return redirect('cart_detail')

def add_rental_extension_cart(request, rental_id):
    cart = Cart(request)
    extension_time = int(request.POST.get("extension_time"))
    cart.add_rental_extension(rental_id, extension_time)
    return redirect('cart_detail')

def add_no_dupe(request, server_id):
    cart = Cart(request)
    server = unrented_server.objects.get(id=server_id)
    cart.add_no_dupe(server=server)
    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    cart = Cart(request)
    return render(request, 'cart.html', dict(cart_items=cart, total=cart.get_overall_rental_cost(), counter=counter))

def remove_cart(request, secondary_id):
    cart = Cart(request)
    server_for_delete = unrented_server.objects.get(secondary_id=secondary_id)
    cart.remove(secondary_id)
    server_for_delete.delete()
    return redirect('cart_detail')

def remove_cart_extension(request, rental_id):
    cart = Cart(request)
    cart.remove(rental_id)
    return redirect('cart_detail')

def empty_cart(request):
    cart = Cart(request)
    for item in cart:
        try:
            item['server'].delete()
        except:
            pass
    cart.clear()
    return redirect('cart_detail')

def payment_detail(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        try:
            decryptor = Fernet(settings.ENC_KEY)
            logged_user = request.user
            payment_detail = payment_details.objects.get(details_owner=logged_user.email)
            card_number = str(decryptor.decrypt(payment_detail.card_number.encode()).decode())
            card_csv = str(decryptor.decrypt(payment_detail.card_csv.encode()).decode())
            card_num_censored = ""
            for num in range(len(card_number) - 4):
                card_num_censored += "*"
            card_num_censored += card_number[len(card_number) - 4:len(card_number)]
            card_end_number =  card_number[len(card_number) - 4:len(card_number)]
            return render(request, 'payment.html', dict(cart=cart, total=cart.get_overall_rental_cost(), existing_details=payment_detail, card_num_censored=card_num_censored, card_end_number=card_end_number))
        except:
            return render(request, 'payment.html', dict(cart=cart, total=cart.get_overall_rental_cost(), existing_details=None, card_num_censored=None, card_end_number=None))
    else:
        print("user not logged in error to be put here")
        return redirect('login')

def save_payment_details(request, card_number, card_csv, exp_year, exp_month):
    encryptor = Fernet(settings.ENC_KEY)
    encrypted_card_num = encryptor.encrypt(card_number.encode())
    encrypted_card_csv = encryptor.encrypt(card_csv.encode())
    try:
        existing_details = payment_details.objects.get(details_owner=request.user.email)
        existing_details.card_number = encrypted_card_num.decode()
        existing_details.card_csv = encrypted_card_csv.decode()
        existing_details.exp_year = exp_year
        existing_details.exp_month = exp_month
        existing_details.save()
    except:
        new_details = payment_details.objects.create(
            details_owner=request.user.email,
            card_number=encrypted_card_num.decode(),
            card_csv=encrypted_card_csv.decode(),
            exp_year=exp_year,
            exp_month=exp_month
        )
        new_details.save()

def pay_with_card(request, card_number, card_csv, exp_year, exp_month):
    cart = Cart(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        charge_token = stripe.Token.create(
            card={
               "number": card_number,
               "exp_month": exp_month,
               "exp_year": exp_year,
               "cvc":card_csv,
            },
        )
        charge_id = stripe.Charge.create(
            amount=int(round(cart.get_overall_rental_cost()*100, 0)),
            currency="eur",
            source=charge_token,
            description="Vortex servers-Server rental:€{} Customer: {}".format(cart.get_overall_rental_cost(), request.user.email)
        )
        product_names = ""
        product_ids = ""
        extensions = ""
        for item in cart:
            try:
                if item['server'] != None:
                    product_names = "Rental: {} for €{}, ".format(item['server'].server_id, item['price'])
                    product_ids = item['server'].secondary_id
                    new_transaction = transaction.objects.create(
                        transaction_amount=float(item['price']),
                        charge_id=charge_id.id,
                        refund_status=False,
                        transaction_owner=request.user.email,
                        transaction_product_names=product_names,
                        transaction_rentals_ids=product_ids,
                        transaction_extensions=extensions
                    )
                    new_transaction.save()
                else:
                    product_names = "Extension: {} months on rental: {} for €{}".format(item['extension'], item['rental_id'], item['price'])
                    current_rental = rental.objects.get(id=int(item['rental_id']))
                    extensions = "{}:{}-{}".format(item['extension'], current_rental.server_id,  item['price'])
                    new_transaction = transaction.objects.create(
                        transaction_amount=float(item['price']),
                        charge_id=charge_id.id,
                        refund_status=False,
                        transaction_owner=request.user.email,
                        transaction_product_names=product_names,
                        transaction_rentals_ids=product_ids,
                        transaction_extensions=extensions
                    )
                    new_transaction.save()
            except:
                product_names = "Extension: {} months on rental: {} for €{}".format(item['extension'], item['rental_id'], item['price'])
                current_rental = rental.objects.get(id=int(item['rental_id']))
                extensions = "{}:{}-{}".format(item['extension'], current_rental.server_id,  item['price'])
                new_transaction = transaction.objects.create(
                    transaction_amount=float(item['price']),
                    charge_id=charge_id.id,
                    refund_status=False,
                    transaction_owner=request.user.email,
                    transaction_product_names=product_names,
                    transaction_rentals_ids=product_ids,
                    transaction_extensions=extensions
                )
                new_transaction.save()
        return charge_id
    except:
        return "error"

def retrieve_card_details(request):
    card_number = request.POST.get("card_num")
    if len(card_number) < 13 or len(card_number) > 19:
        messages.add_message(request, messages.ERROR, "Invalid card details entered")
        return "error"
    card_csv = request.POST.get("csv")
    if len(card_csv) > 4 or len(card_csv) < 3:
        messages.add_message(request, messages.ERROR, "Invalid card details entered")
        return "error"
    exp_month = request.POST.get("exp_month")
    exp_year = request.POST.get("exp_year")
    return [card_number, card_csv, exp_month, exp_year]

def make_extension(request, rental_id, extension, price):
        rental_for_extension = rental.objects.get(id=rental_id)
        rental_for_extension.total_cost += float(price)
        if extension == "Early expiration":
            rental_for_extension.end_time = datetime.datetime.now().date()
            rental_for_extension.expired = True
        else:
            rental_for_extension.end_time += datetime.timedelta(days=(int(extension)*30))
            Outbound.sendRenatalExtension(request)
        rental_for_extension.save()

def create_rentals(request, charge_id):
    cart = Cart(request)
    for item in cart:
        try:
            if item['server'] != None:
                new_rental = rental.objects.create(
                    end_time=datetime.datetime.now()+datetime.timedelta(days=+30),
                    owner=request.user.email,
                    rental_unique_id=id_gens.unique_rental_id_gen(rented_server, unrented_server),
                    total_cost = item['server'].get_rental_cost(),
                    charge_id=charge_id,
                    refund_status = False,
                    server_id=item['server'].secondary_id,
                    expired=False
                )
                new_rental.save()
                Outbound.sendRenatlConfirmation(request, new_rental)
                dupe_to_rented_server = rented_server.objects.create(
                    secondary_id=item['server'].secondary_id,
                    server_id=item['server'].server_id,
                    CPU=item['server'].CPU,
                    motherboard=item['server'].motherboard,
                    RAM=item['server'].RAM,
                    HDD=item['server'].HDD,
                    SSD=item['server'].SSD,
                    GPU=item['server'].GPU,
                    server_owner = request.user.email
                )
                dupe_to_rented_server.save()
                server_for_delete = unrented_server.objects.get(secondary_id=item['server'].secondary_id)
                cart.remove(item['server'].secondary_id)
                if server_for_delete.user_saved == False:
                    server_for_delete.delete()
            else:
                make_extension(request, item['rental_id'], item['extension'], item['price'])
        except:
            make_extension(request, item['rental_id'], item['extension'], item['price'])
    cart.clear()

def checkout(request):
    charge_id = ""
    if request.POST.get("pay_and_save"):
        card = retrieve_card_details(request)
        if card == "error":
            return redirect("payment_detail")
        charge_id = pay_with_card(request, card[0], card[1], card[3], card[2])
        if charge_id == "error":
            return redirect("payment_detail")
        save_payment_details(request, card[0], card[1], card[3], card[2])
    elif request.POST.get("pay_with_card"):
        card = retrieve_card_details(request)
        if card == "error":
            return redirect("payment_detail")
        charge_id = pay_with_card(request, card[0], card[1], card[3], card[2])
        if charge_id == "error":
            return redirect("payment_detail")
    elif request.POST.get("pay_with_existing_card"):
        decryptor = Fernet(settings.ENC_KEY)
        existing_details = payment_details.objects.get(details_owner=request.user.email)
        card_number = str(decryptor.decrypt(existing_details.card_number.encode()).decode())
        card_csv = str(decryptor.decrypt(existing_details.card_csv.encode()).decode())
        charge_id = pay_with_card(request, card_number, card_csv, existing_details.exp_year, existing_details.exp_month)
        if charge_id == "error":
            return redirect("payment_detail")
    create_rentals(request, charge_id)
    return redirect("rental_list")
