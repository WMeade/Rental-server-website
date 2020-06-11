from django.urls import path, include
from .views import display_saved, user_saved, user_shared, display_shared, server_search

urlpatterns = [
    path('saved/',display_saved.as_view(), name= 'display_saved'),
    path('user_saved/<serverid>', user_saved, name='user_saved' ),
    path('user_shared/', user_shared, name='user_shared'),
    path('shared/', display_shared.as_view(),name='shared_display'),
    path('search/', server_search, name='server_search'),


]
