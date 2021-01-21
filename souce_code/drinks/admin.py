from django.contrib import admin
from .models import Drinks
from .models import Brand
# Register your models here.

admin.site.register(Brand)
admin.site.register(Drinks)