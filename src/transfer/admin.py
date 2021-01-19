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


class TransferAllProductDateFilter(admin.SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('All Transfer Date Range')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'docudate'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('today', _('Today')),
			('yesterday', _('Yesterday')),
			('thisweek', _('This week')),
			('lastweek', _('Last week')),
			('thismonth', _('This month')),
			('lastmonth', _('Last month')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either '80s' or '90s')
		# to decide how to filter the queryset.
		from datetime import date
		if self.value() == 'today':
			today = date.today()
			return queryset.filter(created__year=today.year,
								created__month=today.month,
								created__day=today.day).order_by('created')

		if self.value() == 'yesterday':
			import datetime
			today = date.today() - datetime.timedelta(days=1)
			return queryset.filter(created__year=today.year,
								created__month=today.month,
								created__day=today.day).order_by('created')
		
		if self.value() == 'thisweek':
			import datetime
			date = datetime.date.today()
			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created__range=[start_week, end_week]).order_by('created')

		if self.value() == 'lastweek':
			import datetime
			date = datetime.date.today()
			date_lastweek = date - datetime.timedelta(days=7)
			start_week = date_lastweek - datetime.timedelta(date_lastweek.weekday())
			end_week = start_week + datetime.timedelta(7)
			print (start_week, end_week)
			# date = end_week + datetime.timedelta(days=1)
			# start_week = date - datetime.timedelta(date.weekday())
			# end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created__range=[start_week, end_week]).order_by('created')

		if self.value() == 'thismonth':
			today = date.today()
			# print('this month')
			return queryset.filter(created__year=today.year,
								created__month=today.month).order_by('created')

		if self.value() == 'lastmonth':
			import datetime
			today = date.today().replace(day=1) - datetime.timedelta(days=1)
			# print('last month',today)
			return queryset.filter(created__year=today.year,
								created__month=today.month).order_by('created')


class ICStockDetailInline(admin.TabularInline):
	model = ICStockDetail
	fields = ('listno','goodcode','goodname','goodqty','invecode','invename')
	readonly_fields = ('created','updated','user')
	extra = 0 # how many rows to show
	# autocomplete_fields = ('operation','next_pass','next_fail')
	show_change_link = True
	verbose_name = 'Stock Transfer detail'
	verbose_name_plural = 'Stock Transfer detail'

# Register your models here.
@admin.register(ICStockHD)
class ICStockHDAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['docuid','docuno','remark1']
	list_filter = [TransferAllProductDateFilter]
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
	inlines =[ICStockDetailInline]

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