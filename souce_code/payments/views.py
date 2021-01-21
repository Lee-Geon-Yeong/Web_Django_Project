from datetime import datetime

from django.db.models import Prefetch
from django.shortcuts import render
from carts.models import Cart
from payments.models import Payment
# from django.models import Prefetch
from carts.views import cart_total, get_cart_and_items, get_user_cart, clean_cart_view
from django.views.decorators.http import require_GET, require_http_methods
# from django.httpgit.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.views import get_my_cart_list
from drinks.models import Drinks
from accounts.models import Account

# Create your views here.


@login_required
@require_http_methods(['GET', 'POST'])
def create_payment_view(request):
    if request.method == 'GET':

        objects = get_my_cart_list(request)
        total_price = cart_total(request)

        # if not len(objects):
        #     return ValueError()

        if Payment.objects.filter(account=request.user):  # 사용자의 기존 Payment가 존재할 때

            if Payment.objects.filter(is_paid=False).count() == 0:  # 결제 완료된 것밖에 없을 때
                payment = Payment.objects.create(account=request.user, total_price=total_price)  # 사용자의 새로운 Payment 생성
                Payment.total_price = payment.total_price

            else:  # 결제 완료되지 않은 Payment가 존재할 때
                payment = Payment.objects.get(account=request.user, is_paid=False)  # 기존 Payment에 업데이트
                Payment.total_price = update_payment(payment, total_price)

        else:  # 사용자의 기존 Payment가 없을 때 새로 생성
            payment = Payment.objects.create(account=request.user, total_price=total_price)
            Payment.total_price = payment.total_price

        return render(request, template_name="payments/payment_list.html",
                      context={"objects":objects,
                               "total_price":payment.total_price})


def update_payment(payment, total_price):
    payment.total_price = total_price  # cart의 cart_total를 통해 전체 금액 업데이트 후 대입
    payment.save()
    return total_price


def get_user_payment(request):
    items = Payment.objects.filter(account=request.user)
    return items


@login_required
def previous_payment_view(request):
    # 사용자의 Payment중에 is_paid가 True인 거 가져오기
    previous = Payment.objects.filter(account=request.user, is_paid=True)

    return render(request, template_name="payments/previous_list.html",
                  context={"previous":previous})


# 결제 연동 후 처리
def payment_complete(request):
    clean_cart_view(request)
    payment = Payment.objects.get(account=request.user)
    payment.is_paid = True
    payment.save()


def delete_payment():
    pass
