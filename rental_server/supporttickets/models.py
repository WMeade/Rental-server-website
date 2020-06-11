from django.db import models
from rentals.models import transaction
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=255)
    transaction_number = models.CharField(max_length=255)
    description = models.TextField(max_length=450)
    author = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.title+ [{}].format(self.author)

class reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=450)

    def __str__(self):
        return "reply on ticket {} by {}".format(self.ticket, self.author)
