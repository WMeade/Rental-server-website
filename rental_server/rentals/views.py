from django.shortcuts import render, redirect
from payments.cart import Cart
from .models import rental
import datetime
from servers.models import rented_server
from django.template.defaulttags import register
from other_scripts.emailing import Outbound

def rental_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    rental_list = rental.objects.filter(owner=request.user.email)
    servers_rental = {}
    costs_rental = {}
    for server in rental_list:
        if server.expired == False:
            server_current = rented_server.objects.get(secondary_id=server.server_id)
            servers_rental[server.server_id] = server_current.server_id
            costs_rental[server.server_id] = round(server.total_cost, 2)
        else:
            servers_rental[server.server_id] = server.server_id
            costs_rental[server.server_id] = round(server.total_cost, 2)
    return render(request, "rental_list.html", dict(rental_list=rental_list, server_dict=servers_rental, cost_dict=costs_rental))

def rental_detail(request, rental_id):
    current_rental = rental.objects.get(id=rental_id)
    id=""
    if current_rental.expired == False:
        server_current = rented_server.objects.get(secondary_id=current_rental.server_id)
        id = server_current.server_id
    else:
        id=current_rental.rental_unique_id
    total = round(current_rental.total_cost, 2)
    expiry_time = current_rental.end_time - datetime.datetime.now().date()
    return render(request, "rental_detail.html", dict(rental=current_rental, expiry_time=expiry_time, id=id, total=total))

def check_expired():
    rentals = rental.objects.all()
    print("\nrunning expiration check task")
    for current_rental in rentals:
        print("Checking rental: {} for expiration".format(current_rental.id))
        if current_rental.end_time <= datetime.datetime.now().date():
            try:
                server_for_delete = rented_server.objects.get(secondary_id=current_rental.server_id)
                current_rental.expired = True
                Outbound.sendRenatalExpiry(request)
                current_rental.save()
                print("Rental: {} expired, Delete server: {}".format(current_rental.id, server_for_delete.secondary_id))
                server_for_delete.delete()
            except:
                print("Rental: {}  already expired".format(current_rental.id))
                current_rental.expired = True
        else:
            print("Rental: {} not yet expired".format(current_rental.id))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
