from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import unrented_server
from django.db import models


# Create your views here.
class ServerListView(ListView):
    model = unrented_server
    template_name = 'index.html'
    queryset = unrented_server.objects.filter(prebuilt=True)
    context_object_name = 'prebuilt_list'
