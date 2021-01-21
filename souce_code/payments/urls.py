from django.urls import path
from .views import create_payment_view, previous_payment_view

app_name='payments'

urlpatterns = [
    path('', create_payment_view, name='create_payment_view'),
    path('previous/', previous_payment_view, name='previous_payment_view')
]