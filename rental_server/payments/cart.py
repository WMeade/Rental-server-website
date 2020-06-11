from servers.models import unrented_server, rented_server
from rentals.models import rental
from decimal import Decimal
from other_scripts.generators import id_gens

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_rental_extension(self, rental_id, extension_time):
        extension_rental = rental.objects.get(id=rental_id)
        extension_server = rented_server.objects.get(secondary_id=extension_rental.server_id)
        if int(extension_time) > 0:
            price = extension_server.get_rental_cost() * int(extension_time)
            self.cart[str(rental_id)] = {'rental_id': rental_id, 'extension': extension_time, 'price': price, 'rental_unique_id': extension_rental.server_id}
        else:
            price = 199.99
            self.cart[str(rental_id)] = {'rental_id': rental_id, 'extension': "Early expiration", 'price': price, 'rental_unique_id': extension_rental.server_id}
        self.save()

    def add(self, server):
        server_id = str(server.id)
        server_for_dupe = unrented_server.objects.get(id=server_id)
        duplicate_server = unrented_server.objects.create(
        secondary_id=id_gens.duplicate_id_gen(server_id, unrented_server, rented_server),
        server_id=server_for_dupe.server_id,
        CPU=server_for_dupe.CPU,
        motherboard=server_for_dupe.motherboard,
        RAM=server_for_dupe.RAM,
        HDD=server_for_dupe.HDD,
        SSD=server_for_dupe.SSD,
        GPU=server_for_dupe.GPU,
        creator="vortexservers@gmail.com",
        user_made=False,
        user_saved = False,
        shared_publically = False,
        prebuilt=False)
        duplicate_server.save()
        self.cart[str(duplicate_server.secondary_id)] = {'price': str(server.get_rental_cost())}
        self.save()

    def add_no_dupe(self, server):
        self.cart[str(server.secondary_id)] = {'price': str(server.get_rental_cost())}
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, server):
       del self.cart[server]
       self.save()

    def __iter__(self):
        server_ids = self.cart.keys()
        servers = unrented_server.objects.filter(secondary_id__in=server_ids)
        cart = self.cart.copy()
        for server in servers:
            cart[str(server.secondary_id)]['server'] = server
        for server in cart.values():
            server['price'] = round(Decimal(server['price']), 2)
            yield server

    def __len__(self):
        return len(self.cart)

    def get_overall_rental_cost(self):
        return float(round(sum(Decimal(server['price']) for server in self.cart.values()), 2))

    def clear(self):
        del self.session['cart']
        self.save()
