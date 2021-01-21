from django import forms
from carts.models import CartItem

class CartItemUpdateForm(forms.Form):
    quantity = forms.IntegerField(max_value=20, min_value=0)

