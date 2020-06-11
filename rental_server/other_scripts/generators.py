import string
import random

class id_gens:

    @staticmethod
    def unique_rental_id_gen(rented_server, unrented_server):
        characters = string.printable
        is_unique = False
        while is_unique == False:
            token = ""
            for i in range (0, 26 + (len(rented_server.objects.all())//3)):
                token += characters[random.randint(0, 99)]
            rented_servers = rented_server.objects.all()
            unrented_servers = unrented_server.objects.all()
            for i in rented_servers:
                if i.server_id == token:
                    pass
                else:
                    is_unique = True
            for i in unrented_servers:
                if i.server_id == token:
                    pass
                else:
                    is_unique = True
        return token

    @staticmethod
    def duplicate_id_gen(server_id,unrented_server, rented_server):
        characters = string.ascii_lowercase
        unrented_servers = unrented_server.objects.all()
        rented_servers = rented_server.objects.all()
        is_unique = False
        while is_unique == False:
            token = server_id + "_"
            for i in range (0, 26 + (len(rented_server.objects.all())//3)):
                token += characters[random.randint(0, 25)]
            for i in unrented_servers:
                if i.server_id == token:
                    is_unique = False
                else:
                    is_unique = True
            for i in rented_servers:
                if i.server_id == token:
                    is_unique = False
                else:
                    is_unique = True
        return token

    @staticmethod
    def new_id_gen(unrented_server, rented_server):
        characters = string.ascii_lowercase
        unrented_servers = unrented_server.objects.all()
        rented_servers = rented_server.objects.all()
        is_unique = False
        while is_unique == False:
            token = ""
            for i in range (0, 26 + (len(rented_server.objects.all())//3)):
                token += characters[random.randint(0, 25)]
            for i in unrented_servers:
                if i.server_id == token:
                    pass
                else:
                    is_unique = True
            for i in rented_servers:
                if i.server_id == token:
                    is_unique = False
                else:
                    is_unique = True
        return token
