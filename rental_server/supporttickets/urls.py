from django.urls import path ,include
from .views import transaction_view, create_ticket_view, create_ticket, ticket_view, transaction_search, ticket_detail, reply_ticket, resolve_ticket, refund_ticket, delete_reply, refund_transaction

urlpatterns = [
    path('transactions/', transaction_view, name='transactions'),
    path('create_ticket_form/<transaction_id>', create_ticket_view, name='create_ticket_form'),
    path('create_ticket/<transaction_id>', create_ticket, name='create_ticket'),
    path('tickets/', ticket_view, name="tickets"),
    path('searchtransaction/', transaction_search, name="transaction_search"),
    path('ticket_detail/<ticket_id>', ticket_detail, name="ticket_detail"),
    path('reply/<ticket_id>', reply_ticket, name="reply"),
    path('refund/<ticket_id>', refund_ticket, name="refund"),
    path('refund<transaction_id>', refund_transaction, name="refund_transaction"),
    path('resolve_ticket/<ticket_id>', resolve_ticket, name="resolve_ticket"),
    path('delete_reply/<reply_id>', delete_reply, name="delete_reply"),
]
