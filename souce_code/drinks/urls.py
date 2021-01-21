from django.urls import path
from drinks.views import list_filter_view,brand_detail_view, drink_detail_view

app_name='drinks'

urlpatterns = [
    path('', list_filter_view, name='list_view'),
    path('brand/<str:brand_name>/', brand_detail_view,name='brand_detail_view'),
    path('<int:pk>/', drink_detail_view, name='detail_view'),
]