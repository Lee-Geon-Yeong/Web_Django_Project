from django import forms
from carts.models import CartItem


class CartItemCreateForm(forms.Form):
    quantity = forms.IntegerField(max_value=20, min_value=1)
