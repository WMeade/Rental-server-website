from django.db import models


class payment_details(models.Model):
    details_owner = models.EmailField()
    card_number = models.TextField()
    card_csv = models.TextField()
    exp_month = models.TextField()
    exp_year = models.TextField()

    def __str__(self):
        return "Payment details: {}".format(self.details_owner)
