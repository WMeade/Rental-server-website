from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from other_scripts.emailing import Outbound
from payments.cart import Cart
from servers.models import unrented_server
from django.contrib import messages
from users.models import CustomUser
from payments.views import retrieve_card_details, save_payment_details
from payments.models import payment_details
from cryptography.fernet import Fernet
from rental_Server import settings

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self,form):
        Outbound.sendSignUpConfirmation(self.request, form.instance.username, form.instance.email)
        return super().form_valid(form)

def logout_clear_cart(request):
    cart = Cart(request)
    for item in cart:
        try:
            server_for_delete = unrented_server.objects.get(secondary_id=item['server'].secondary_id)
            if not server_for_delete.user_saved:
                server_for_delete.delete()
        except:
            print("Not a server")
    return redirect("logout")

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "edit_profile.html", dict(user=CustomUser.objects.get(username=request.user.username)))

def change_password(request):
    return render(request, "change_password.html", dict(user=CustomUser.objects.get(username=request.user.username)))

def edit_payment_details(request):
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
        return render(request, "edit_card_details.html", dict(existing_details=payment_detail, card_num_censored=card_num_censored, card_end_number=card_end_number))
    except:
        return render(request, 'edit_card_details.html', dict(existing_details=None, card_num_censored=None, card_end_number=None))

def make_profile_edit(request):
    current_user = CustomUser.objects.get(username=request.user.username)
    if request.POST.get("password1") == request.POST.get("password2") and current_user.check_password(request.POST.get("password1")):
        current_user.username = request.POST.get("username")
        current_user.email = request.POST.get("email")
        current_user.fname = request.POST.get("fname")
        current_user.lname = request.POST.get("lname")
        current_user.dob = request.POST.get("dob")
        current_user.address1 = request.POST.get("address1")
        current_user.address2 = request.POST.get("address2")
        current_user.address3 = request.POST.get("address3")
        try:
            Outbound.sendEditProfile(request)
            current_user.save()
        except:
            messages.add_message(request, messages.ERROR, "Date of birth must be filled in!")
            return redirect("edit_profile")
    else:
        messages.add_message(request, messages.ERROR, "Password Invalid")
    return redirect("edit_profile")

def make_change_password(request):
    current_user = CustomUser.objects.get(username=request.user.username)
    if current_user.check_password(request.POST.get("password1")):
        if request.POST.get("password2") == request.POST.get("password3"):
            current_user.set_password(request.POST.get("password2"))
            Outbound.sendEditProfilePassword(request)
            current_user.save()
            return redirect("login")
        else:
            messages.add_message(request, messages.ERROR, "New passwords do not match!")
            return redirect("change_password")
    else:
        messages.add_message(request, messages.ERROR, "Password Incorrect")
        return redirect("change_password")

def make_change_card_details(request):
    card = retrieve_card_details(request)
    if card != "error":
        Outbound.sendEditProfileCard(request)
        save_payment_details(request, card[0], card[1], card[3], card[2])
    return redirect("edit_payment_details")
