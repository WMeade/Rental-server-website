from django.urls import path

from .views import SignUpView, logout_clear_cart, edit_profile, make_profile_edit, change_password, make_change_password, make_change_card_details, edit_payment_details

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout_clear_cart/', logout_clear_cart, name='logout_clear_cart'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edit_profile/make_edit' ,make_profile_edit, name='make_edit'),
    path('edit_profile/change_password', change_password, name="change_password"),
    path('edit_profile/make_change_password', make_change_password, name="make_change_password"),
    path('edit_profile/edit_payment_details', edit_payment_details, name="edit_payment_details"),
    path('edit_profile/make_change_card_details', make_change_card_details, name='make_change_card_details')

]
