from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.forms import SocialUserUpdateForm
from carts.forms import CartItemUpdateForm
# from carts.views import get_cart_and_items
from allauth.account import urls
from allauth import urls


@login_required
@require_http_methods(['GET', 'POST'])
def social_account_update_view(request):
    if not request.user.age:
        if request.method == "POST":
            form = SocialUserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.instance.save()
                return HttpResponseRedirect('/mypage/')
            else:
                return HttpResponseRedirect('/mypage/')
        else:
            form = SocialUserUpdateForm(instance=request.user)
            return render(request, 'account/socialupdate.html', {'form': form})
    return HttpResponseRedirect('/')


@login_required
@require_GET
def my_page_view(request):
    cart = get_my_cart_list(request)
    update_form = CartItemUpdateForm()
    return render(request,
                  'account/mypage.html',
                  context={
                      'objects': cart,
                      'update_form': update_form
                  })


def get_my_cart_list(request):
    cart = request.user.cart
    items = request.user.cart.items.all().select_related('drink')
    return items
