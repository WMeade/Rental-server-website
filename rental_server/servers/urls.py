from django.urls import path, include
from servers.views import ServerListView

urlpatterns = [
    path('', ServerListView.as_view(), name='home'),
    path('cart/', include('payments.urls')),
    path('customize_server/', include('customize_server.urls')),
    path('support/',include('supporttickets.urls'))
]
