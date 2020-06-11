from django.db import models
from other_scripts.generators import id_gens

class server_component(models.Model):
    part_id = models.TextField(max_length=20)
    part_type = models.TextField()
    rental_cost = models.FloatField()
    hardware_cost = models.FloatField()
    specifications = models.TextField()
    socket_type = models.TextField(default=None)

    def get_rental_cost(self):
        return self.rental_cost

    def get_type(self):
        return self.part_type

    def get_hardware_cost(self):
        return self.hardware_cost

    def get_specifications(self):
        return self.specifications

    def get_socket(self):
        return self.socket_type

    def __str__(self):
        return self.part_id + " ({})".format(self.part_type)


class rented_server(models.Model):
    secondary_id=models.TextField()
    server_id = models.TextField()
    CPU = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='CPU_rented')
    motherboard = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='motherboard_rented')
    RAM = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='RAM_rented')
    HDD = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='HDD_rented')
    SSD = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='SSD_rented')
    GPU = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='GPU_rented')
    server_owner = models.EmailField()

    def get_rental_cost(self):
        rental_cost = 50.00 + self.CPU.get_rental_cost() + self.motherboard.get_rental_cost() + self.RAM.get_rental_cost() + self.HDD.get_rental_cost() + self.SSD.get_rental_cost()
        return round(rental_cost,2)

    def set_CPU(self, cpu):
        self.CPU = cpu
        self.save()

    def set_motherboard(self, mb):
        self.motherboard = mb
        self.save()

    def set_RAM(self, ram):
        self.RAM = ram
        self.save()

    def set_HDD(self, hdd):
        self.HDD = hdd
        self.save()

    def set_SSD(self, ssd):
        self.SSD = ssd
        self.save()

    def get_server_id(self):
        return self.server_id

    def get_server_owner(self):
        return self.server_owner

    def delete_server(self):
        self.delete()

    def __str__(self):
        return "{} - ID: {}".format(self.server_id, self.secondary_id)

class unrented_server(models.Model):
    secondary_id=models.TextField()
    server_id = models.TextField()
    CPU = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='CPU')
    motherboard = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='motherboard')
    RAM = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='RAM')
    HDD = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='HDD')
    SSD = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='SSD')
    GPU = models.ForeignKey(server_component, on_delete=models.CASCADE, related_name='GPU')
    creator = models.EmailField(default=None)
    user_made = models.BooleanField(default=False)
    user_saved = models.BooleanField(default=False)
    shared_publically = models.BooleanField(default=False)
    prebuilt = models.BooleanField(default=True)

    def get_rental_cost(self):
        rental_cost = 50.00 + self.CPU.get_rental_cost() + self.motherboard.get_rental_cost() + self.RAM.get_rental_cost() + self.HDD.get_rental_cost() + self.SSD.get_rental_cost()
        return round(rental_cost, 2)

    def set_CPU(self, cpu):
        self.CPU = cpu
        self.save()

    def set_motherboard(self, mb):
        self.motherboard = mb
        self.save()

    def set_RAM(self, ram):
        self.RAM = ram
        self.save()

    def set_HDD(self, hdd):
        self.HDD = hdd
        self.save()

    def set_SSD(self, ssd):
        self.SSD = ssd
        self.save()

    def get_server_id(self):
        return self.server_id

    def get_server_creator(self):
        return self.creator

    def get_prebuilt(self):
        return self.prebuilt

    def delete_server(self):
        self.delete()

    def __str__(self):
        return self.server_id
