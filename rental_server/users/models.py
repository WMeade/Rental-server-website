from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    fname = models.CharField(null=True, blank=True, max_length=255)
    lname = models.CharField(null=True, blank=True, max_length=255)
    dob = models.DateField(null=True, blank=True,)
    address1 = models.CharField(null=True, blank=True, max_length=255)
    address2 = models.CharField(null=True, blank=True, max_length=255)
    address3 = models.CharField(null=True, blank=True, max_length=255)

