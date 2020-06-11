"""rental_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from threading import Thread
import time
from rentals.views import check_expired
from shared_server.views import display_saved

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('servers.urls')),
    path('rentals/', include('rentals.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name = 'home'),
    path('saved/', include('shared_server.urls')),
]

def check_for_expiries():
    while True:
        check_expired()
        time.sleep(60*60)

check_expiry_thread = Thread(target=check_for_expiries)
check_expiry_thread.start()
