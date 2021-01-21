from django.urls import path
from accounts.views import my_page_view,social_account_update_view

app_name='mypage'

urlpatterns = [
    path('', my_page_view, name='index'),
    path('socialupdate/',social_account_update_view, name='social_update'),
]