from django.contrib import admin
from .models import *


class PromotionAdmin(admin.ModelAdmin):
    list_display = ['promotion_name', 'promotiondate']


admin.site.register(Promotion, PromotionAdmin)
# Register your models here.
