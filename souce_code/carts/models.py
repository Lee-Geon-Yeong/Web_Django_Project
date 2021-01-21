from django.db import models
from django.conf import settings
from drinks.models import Drinks
from payments.models import Payment

class Cart(models.Model):
    total_price = models.PositiveIntegerField(default=None, null=True)
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    drink = models.ForeignKey(to=Drinks, on_delete=models.CASCADE, related_name="payments")
    quantity = models.PositiveIntegerField(default=None, null=True)
    cart = models.ForeignKey(to=Cart, on_delete=models.DO_NOTHING, related_name='items')
    price = models.PositiveIntegerField(default=0, null=True)
    payment = models.ForeignKey(to=Payment, on_delete=models.CASCADE, related_name="items", default=None, null=True)
