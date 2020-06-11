from django.contrib import admin
from rentals.models import rental, transaction


admin.site.register(rental)
admin.site.register(transaction)
