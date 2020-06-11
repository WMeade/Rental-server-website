from rentals.models import transaction, rental
from servers.models import rented_server
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, reply
import stripe
from rental_Server import settings
import datetime
from other_scripts.emailing import Outbound

def transaction_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        transactions = transaction.objects.all()
    else:
        transactions = transaction.objects.filter(transaction_owner=request.user.email)
    return render(request, "transaction_list.html", dict(transactions=transactions))

def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    replies = reply.objects.filter(ticket=ticket)
    return render(request, "ticket_detail.html", dict(ticket=ticket, replies=replies))

def reply_ticket(request, ticket_id):
    current_ticket = Ticket.objects.get(id=ticket_id)
    new_reply = reply.objects.create(
        ticket=current_ticket,
        author=request.user,
        text=request.POST.get('text')
    )
    new_reply.save()
    return redirect("ticket_detail", ticket_id=ticket_id)


def ticket_view(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(author=request.user)
    return render(request, "ticket_list.html", dict(tickets=tickets))


def create_ticket_view(request, transaction_id):
    return render(request, "ticket_create.html", dict(transaction_id=transaction_id, ticket_owner=request.user))

def create_ticket(request, transaction_id):
    new_ticket = Ticket.objects.create(
        title = request.POST.get('title'),
        transaction_number = transaction_id,
        description = request.POST.get('description'),
        author = request.user
    )
    Outbound.sendTicketCreateConfirmation(request, new_ticket.title)
    new_ticket.save()
    return redirect("tickets")

def transaction_search(request):
    search_id = request.POST.get('search_bar')
    query_list = transaction.objects.all()
    transactions = []
    for query in query_list:
        if str(query.id).find(search_id) != -1:
            transactions.append(query)
    return render(request, "transaction_list.html", dict(transactions=transactions))

def resolve_ticket(request, ticket_id):
    current_ticket = Ticket.objects.get(id=ticket_id)
    Outbound.sendTicketClosedConfirmation(request, current_ticket)
    current_ticket.delete()
    return redirect("tickets")

def refund_ticket(request, ticket_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    current_ticket = Ticket.objects.get(id=ticket_id)
    refund_transaction = transaction.objects.get(id=current_ticket.transaction_number)
    refund_transaction.refund_status = True
    refund_transaction.save()
    transaction_products = refund_transaction.transaction_rentals_ids.split(',')
    for string in transaction_products:
        string = string.replace(" ", "")
        if string == "":
            break
        current_rental = rental.objects.get(server_id=string)
        current_rental.expired = True
        current_rental.end_time = datetime.datetime.now().date()
        current_rental.save()
    transaction_extensions = refund_transaction.transaction_extensions.split(',')
    for string in transaction_extensions:
        string = string.replace(" ", "")
        if string == "":
            break
        extension_months = string[0: string.index(":")]
        extension_server_id = string[string.index(":") + 1: string.index("-")]
        current_rental = rental.objects.get(server_id=extension_server_id)
        current_rental.end_time -= datetime.timedelta(days=(int(extension_months)*30))
        current_rental.total_cost -= float(string[string.index("-") + 1:])
        current_rental.save()

    stripe.Refund.create(
        charge = refund_transaction.charge_id,
        amount = int(refund_transaction.transaction_amount*100)
    )
    current_ticket.delete()
    return redirect("tickets")

def refund_transaction(request, transaction_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    refund_transaction = transaction.objects.get(id=transaction_id)
    refund_transaction.refund_status = True
    refund_transaction.save()
    transaction_products = refund_transaction.transaction_rentals_ids.split(',')
    for string in transaction_products:
        string = string.replace(" ", "")
        if string == "":
            break
        current_rental = rental.objects.get(server_id=string)
        current_rental.expired = True
        current_rental.end_time = datetime.datetime.now().date()
        current_rental.save()
    transaction_extensions = refund_transaction.transaction_extensions.split(',')
    for string in transaction_extensions:
        string = string.replace(" ", "")
        if string == "":
            break
        extension_months = string[0: string.index(":")]
        extension_server_id = string[string.index(":") + 1: string.index("-")]
        current_rental = rental.objects.get(server_id=extension_server_id)
        current_rental.end_time -= datetime.timedelta(days=(int(extension_months)*30))
        current_rental.total_cost -= float(string[string.index("-") + 1:])
        current_rental.save()
    stripe.Refund.create(
        charge = refund_transaction.charge_id,
        amount = int(refund_transaction.transaction_amount*100)
    )
    return redirect("transactions")

def delete_reply(request, reply_id):
    current_reply = reply.objects.get(id=reply_id)
    ticket = current_reply.ticket.id
    current_reply.delete()
    return redirect("ticket_detail", ticket_id=ticket)
