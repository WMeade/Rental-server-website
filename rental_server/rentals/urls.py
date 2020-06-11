from django.urls import path, include
from .views import rental_view, rental_detail

urlpatterns = [
    path("rental_view/", rental_view, name="rental_list"),
    path("rental_detail/<rental_id>", rental_detail, name="rental_detail")
]
