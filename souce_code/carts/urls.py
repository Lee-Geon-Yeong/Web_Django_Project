from django.urls import path
from .views import item_update_view, item_delete_view

app_name='carts'

urlpatterns = [
    path('items/<int:pk>/', item_update_view, name='item_update_view'),
    path('items/delete/<int:pk>/', item_delete_view, name='item_delete_view')
]