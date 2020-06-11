from django.shortcuts import render, redirect
from servers.models import server_component, unrented_server, rented_server
from other_scripts.generators import id_gens
from payments.cart import Cart
from decimal import Decimal

def select_cpu(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cpu_list = server_component.objects.filter(part_type="CPU")
    return render(request, "cpu_select.html", dict(cpu_list=cpu_list))

def select_comps(request):
    cpu = server_component.objects.get(id=request.POST.get("cpu"))
    components_with_socket = server_component.objects.filter(socket_type=cpu.socket_type)
    motherboards = []
    ram = []
    for component in components_with_socket:
        if component.part_type == "MOTHERBOARD":
            motherboards.append(component)
    ram_list = server_component.objects.filter(part_type="RAM")
    motherboard_max_dimm = int(motherboards[0].specifications)
    for motherboard in motherboards:
        if int(motherboard.specifications) > motherboard_max_dimm:
            motherboard_max_dimm = int(motherboard.specifications)
    for ram_module in ram_list:
        if int(ram_module.specifications) <= motherboard_max_dimm:
            ram.append(ram_module)
    hdd = server_component.objects.filter(part_type="HDD")
    ssd = server_component.objects.filter(part_type="SSD")
    gpu = server_component.objects.filter(part_type="GPU")
    return render(request, "select_comps.html", dict(cpu=cpu, motherboard_list=motherboards, ram_list=ram, hdd_list=hdd, ssd_list=ssd, gpu_list=gpu))

def edit_comps(request):
    server_edit = unrented_server.objects.get(id=request.POST.get("user_made_edit"))
    if  request.POST.get('save_selected'):
        serverid = request.POST.get("user_made_edit")
        return redirect("user_saved", serverid=serverid)
    elif request.POST.get("edit_selected"):
        cpu = server_edit.CPU
        components_with_socket = server_component.objects.filter(socket_type=cpu.socket_type)
        motherboards = []
        for component in components_with_socket:
            if component.part_type == "MOTHERBOARD":
                motherboards.append(component)
        ram = server_component.objects.filter(part_type="RAM")
        hdd = server_component.objects.filter(part_type="HDD")
        ssd = server_component.objects.filter(part_type="SSD")
        gpu = server_component.objects.filter(part_type="GPU")
        return render(request, "edit_comps.html", dict(cpu=cpu, motherboard_list=motherboards, ram_list=ram, hdd_list=hdd, ssd_list=ssd, gpu_list=gpu, server_edit=server_edit))

def finalize_edit(request, server_id):
    cart = Cart(request)
    name = request.POST.get("server_id")
    motherboard = server_component.objects.get(id=request.POST.get("motherboard"))
    ram = server_component.objects.get(id=request.POST.get("ram"))
    hdd = server_component.objects.get(id=request.POST.get("hdd"))
    ssd = server_component.objects.get(id=request.POST.get("ssd"))
    gpu = server_component.objects.get(id=request.POST.get("gpu"))
    edited_server = unrented_server.objects.get(id=server_id)
    edited_server.motherboard = motherboard
    edited_server.RAM = ram
    edited_server.HDD = hdd
    edited_server.SSD = ssd
    edited_server.GPU = gpu
    edited_server.server_id = name
    edited_server.save()
    cart.remove(edited_server.secondary_id)
    cart.add_no_dupe(edited_server)
    return redirect("cart_detail")


def summary(request, cpu_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart(request)
    name = request.POST.get("server_id")
    cpu = server_component.objects.get(id=cpu_id)
    motherboard = server_component.objects.get(id=request.POST.get("motherboard"))
    ram = server_component.objects.get(id=request.POST.get("ram"))
    hdd = server_component.objects.get(id=request.POST.get("hdd"))
    ssd = server_component.objects.get(id=request.POST.get("ssd"))
    gpu = server_component.objects.get(id=request.POST.get("gpu"))
    new_server = unrented_server.objects.create(
        secondary_id=id_gens.new_id_gen(unrented_server, rented_server),
        server_id = name,
        CPU = cpu,
        motherboard = motherboard,
        RAM = ram,
        HDD= hdd,
        SSD = ssd,
        GPU = gpu,
        creator = request.user.email,
        user_made = True,
        user_saved = False,
        shared_publically = False,
        prebuilt = False
     )
    new_server.save()
    cart.add_no_dupe(new_server)
    return redirect("cart_detail")

def delete_and_do_something(request, secondary_id, route):
    server_for_delete = unrented_server.objects.get(secondary_id=secondary_id)
    server_for_delete.delete()
    if route == "try_again":
        return redirect("select_cpu")
    elif route == "home":
        return redirect("home")
