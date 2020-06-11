from django.db import models
from servers.models import rented_server
import datetime
import django.utils.timezone as date

class rental(models.Model):
    start_time = models.DateField(auto_now=True)
    end_time = models.DateField()
    owner = models.EmailField()
    rental_unique_id = models.TextField()
    total_cost = models.FloatField()
    charge_id = models.TextField()
    refund_status = models.BooleanField()
    server_id = models.TextField()
    expired = models.BooleanField()

    def increase_end_time(self, days):
       self.end_time += days

    def get_end_date(self):
        return self.end_time

    def get_owner(self):
        return self.owner

    def get_rental_id(self):
        return self.rental_unique_id

    def get_total_cost(self):
        current_rented_server = rented_server.objects.get(__server_id=self.server_id)
        self.total_cost = current_rented_server.get_rental_cost() * (self.end_time - self.start_time)
        self.save()
        return self.total_cost()

    def get_refund_status(self):
        return self.refund_status

    def get_start_date(self):
        return self.start_time

    def set_charge_id(self, charge_id):
        self.charge_id = charge_id

    def get_server_id(self):
        return self.server_id

    def __str__(self):
        return "Rental: {} Owner: {} start: {} end: {} - ID: {}".format(self.rental_unique_id, self.owner, self.start_time, self.end_time, self.id)

class transaction(models.Model):
    transaction_amount = models.FloatField()
    transaction_time = models.DateField(auto_now=True)
    charge_id = models.TextField()
    refund_status = models.BooleanField()
    transaction_owner = models.EmailField()
    transaction_product_names = models.TextField()
    transaction_rentals_ids = models.TextField()
    transaction_extensions = models.TextField()

    def __str__(self):
        return "Transaction owner: {}, Transaction amount: €{}, Transaction time: {} - {}".format(self.transaction_owner, self.transaction_amount/100, self.transaction_time, self.transaction_product_names)
