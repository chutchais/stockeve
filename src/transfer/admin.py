from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import date
# Register your models here.
# from .models import Sale,SaleChildDetail,SoInvHD,SoInvDT
# from product.models import ProductStock,Product

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from transfer.models import ICStockHD,ICStockDetail

# Register your models here.
@admin.register(ICStockHD)
class ICStockHDAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['docuid','docuno']
	# list_filter = [SaleAllProductDateFilter]
	list_display = ('docuid','docuno','remark1','docudate','created')
	readonly_fields = ('created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True
	ordering = ['-docudate','docuid']

	fieldsets = [
		('Basic Information',{'fields': ['docuid','docuno','remark1','docudate']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	# resource_class      = SaleResource
	# inlines =[OrderDetailInline]

@admin.register(ICStockDetail)
class ICStockDetailAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['icstockhd__docuid','icstockhd__docuno','goodcode','goodname']
	list_filter = ['invecode']#SaleAllProductDateFilter]
	list_display = ('icstockhd','listno','goodcode','goodname','goodqty','invecode')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['product']
	readonly_fields = ('updated','user','created')
	ordering = ['-created','icstockhd','listno']

	fieldsets = [
		('Basic Information',{'fields': ['icstockhd','listno','goodid','goodcode','goodname']}),
		('Price',{'fields': ['goodqty','inveid','invecode','invename']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]