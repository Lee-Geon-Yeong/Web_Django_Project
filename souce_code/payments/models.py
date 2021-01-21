from django.db import models
from django.conf import settings

# use payment as 찜목록
class Payment(models.Model):
    is_paid = models.BooleanField(default=False, null=False)
    account = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='payments', null=True, default=None)
    total_price = models.PositiveIntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="paid date",null=True,default=None)
