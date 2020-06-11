from django.shortcuts import render, redirect
from other_scripts.generators import id_gens
from django.shortcuts import render
from django.views.generic import ListView
from django.db import models
from servers.models import unrented_server, rented_server
from django.db.models import Q
from other_scripts.emailing import Outbound



class display_saved(ListView):
    model = unrented_server
    template_name = 'saved_detail.html'
    queryset = unrented_server.objects.filter(user_saved=True)
    context_object_name = 'saved_list'




class display_shared(ListView):
    model = unrented_server
    template_name = 'shared_servers.html'
    queryset = unrented_server.objects.filter(shared_publically = True)
    context_object_name = 'shared_list'


def user_saved(request, serverid):
    print(serverid)
    server = unrented_server.objects.get(id=serverid)
    server_copy = unrented_server.objects.create(
        secondary_id=id_gens.new_id_gen(unrented_server,  rented_server),
        server_id=server.server_id,
        CPU=server.CPU,
        motherboard=server.motherboard,
        RAM = server.RAM,
        HDD=server.HDD,
        SSD=server.SSD,
        GPU=server.GPU,
        creator=server.creator,
        user_made=True,
        user_saved=True,
        shared_publically=False,
        prebuilt=False)
    server_copy.save()
    Outbound.sendSharingServer(request)
    return redirect("cart_detail")

def user_shared(request):
    serverid = request.POST.get("user_select")
    server = unrented_server.objects.get(id=serverid)
    if  request.POST.get('share_server'):
        server.shared_publically = True
        server.save()
        return redirect("shared_display")
    elif request.POST.get('unsave_server'):
        server.user_saved = False
        server.shared_publically = False
        server.save()
        return redirect("display_saved")
    elif request.POST.get('unshare_server'):
        server.shared_publically = False
        server.save()
        return redirect("display_saved")


def server_search(request):
    search_id = request.POST.get('search_bar')
    query_list = unrented_server.objects.filter(shared_publically=True)
    servers = []
    for query in query_list:
        components = query.CPU.part_id + query.motherboard.part_id + query.RAM.part_id + query.HDD.part_id + query.SSD.part_id + query.GPU.part_id
        if components.upper().find(search_id.upper()) !=-1:
            servers.append(query)

    return render(request, "shared_servers.html", dict(shared_list=servers))
