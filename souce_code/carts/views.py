from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from drinks.models import Drinks
from django.db.models import Q, Prefetch
from carts.forms import CartItemUpdateForm
from django.urls import reverse_lazy
from accounts.views import get_my_cart_list
from payments.models import Payment

# Create your views here.
@require_http_methods(['POST'])
def item_update_view(request, pk):
    cart_item = CartItem.objects.get(id=pk)
    if request.method == "POST":
        form = CartItemUpdateForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity == 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
    return HttpResponseRedirect(reverse_lazy('mypage:index'))
@login_required
@require_http_methods(['POST'])
def item_delete_view(request, pk):
    item = CartItem.objects.get(id=pk)
    item.delete()
    return HttpResponseRedirect(reverse_lazy('mypage:index'))

@login_required
@require_http_methods(["POST"])
def clean_cart_view(request):
    if Payment.is_paid:
        items = CartItem.objects.get(user=request.user)
        for item in items:
            item.delete()


# help functions
def create_cart_item(drink_id, quantity, cart):
    for item in cart.items.all():
        if item.drink.id == drink_id:
            obj = CartItem.objects.get(drink=Drinks.objects.get(id=drink_id),cart=cart)
            if (obj.quantity + quantity < 21):
                obj.quantity += quantity
                obj.save()
            return obj
    drink = Drinks.objects.get(id=drink_id)
    obj = CartItem.objects.create(drink=drink,cart=cart,quantity=quantity,price=drink.price)
    obj.save()
    return obj

def get_user_cart(request):
    return Cart.objects.get(user=request.user)

def update_cart_item(pk, quantity):
    item = CartItem.objects.get(id=pk)
    item.quantity = quantity
    item.save()

    
def get_cart_and_items(request):
    objects = Cart.objects.prefetch_related(Prefetch('items')).get(user=request.user)
    return objects

def copy_cart_to_payment(request):
    pass


def cart_total(request, total=0):

    cartitems = get_my_cart_list(request)

    for cartitem in cartitems:
        total += cartitem.drink.price * cartitem.quantity

    return total

