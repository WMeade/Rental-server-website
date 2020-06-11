from django.urls import path, include
from .views import select_cpu, select_comps, summary, delete_and_do_something, edit_comps, finalize_edit


urlpatterns = [
    path('select_cpu/',select_cpu, name='select_cpu'),
    path('select_comps/', select_comps, name='select_comps'),
    path('summary/<int:cpu_id>', summary, name='summary'),
    path('redirecttochoice/<secondary_id>/<route>', delete_and_do_something, name="del_and_do"),
    path('edit_comps/', edit_comps, name="edit_comps"),
    path('edit_comps/finalize_edit/<server_id>', finalize_edit, name="finalize_edit")
]
