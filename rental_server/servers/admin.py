from django.contrib import admin
from servers.models import server_component, rented_server, unrented_server

admin.site.register(server_component)
admin.site.register(rented_server)
admin.site.register(unrented_server)