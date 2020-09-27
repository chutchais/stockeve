from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import date
# Register your models here.
from .models import Sale,SaleChildDetail,SoInvHD
from product.models import ProductStock,Product

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

# Modify by Chutchai on June 14,2020
#To support Sale multiple product
class SaleResource(resources.ModelResource):
	class Meta:
		model = Sale
		import_id_fields = ()
		skip_unchanged = True
		report_skipped= True
		exclude = ('id','user','productstock','created','updated','status' )


class SaleAllProductDateFilter(admin.SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('All Product Date Range')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'created'

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

# @admin.enable_action('delete_selected')
@admin.register(Sale)
class SaleAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','title','product__name']
	list_filter = [SaleAllProductDateFilter]
	list_display = ('product','store','qty','price','salename','balance','created','status')
	# list_editable = ('color','move_performa')
	autocomplete_fields = ['product']
	readonly_fields = ('balance','created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['product','store','qty','price','description','salename']}),
		('Stock',{'fields': ['balance']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	resource_class      = SaleResource

	# class Meta:
	# 	widgets = { 'productstock': forms.Select(attrs={'width': 200})}
	

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(SaleAdmin, self).save_model(request, obj, form, change)

# Not impact with Autocompleted Select
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		# if db_field.name == 'product':
		# 	kwargs["queryset"] = Product.objects.filter(finished_goods = True,
		# 												status = True)
		# if db_field.name == 'productstock':
		# 	kwargs["queryset"] = ProductStock.objects.filter(store__sale_able = True)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SaleChildDetail)
class SaleChildSummaryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	change_list_template = 'admin/sale_child_product_change_list.html'
	# date_hierarchy = 'rent_date'
	# date_hierarchy_drilldown = False
	search_fields = ['product__number','description']
	list_filter = [SaleAllProductDateFilter]
	# actions =['delete_selected']
	resource_class      = SaleResource


	def changelist_view(self, request, extra_context=None):
		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		try:
			qs = response.context_data['cl'].queryset
		except (AttributeError, KeyError):
			return response

		# metrics = {
		# 	'total_containers' : Count('container'),
		# 	'total_handling_time' : Sum('che__kind__handling_time'),
		# 	'transportation_time' : Max('che__kind__trans_time'),
		# 	'total_minutes' : F('total_handling_time')+F('transportation_time'),
		# 	'mod_minute' : Floor(F('total_minutes')/60),
		# 	'total_hours' : Floor(F('total_minutes')/60)
		# }
		# reports     = qs.values('terminal','rent_date__date',
		# 					'che__kind').annotate(
		# 					**metrics).order_by(
		# 					'terminal','rent_date__date',
		# 					'che__kind'
		# 					)
		
		# for r in reports:
		# 	mod_minute = r['total_minutes'] % 60
		# 	hours   = math.floor(r['total_minutes'] / 60)
		# 	hours   = hours + (0.5 if mod_minute > 0 and mod_minute < 30 else 0)
		# 	hours   = hours + (1 if mod_minute >= 30 else 0)
		# 	r['mod_minute'] = mod_minute
		# 	r['total_hours'] = hours
		reports     = qs

		response.context_data['summary']=list(reports)
		return response


@admin.register(SoInvHD)
class SoInvHDAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['soinvid','docuno']
	# list_filter = [SaleAllProductDateFilter]
	list_display = ('soinvid','docuno','totabaseamnt','vatamnt','netamnt','saledate')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['product']
	readonly_fields = ('created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['soinvid','docuno','saledate']}),
		('Price',{'fields': ['totabaseamnt','vatamnt','netamnt']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	# resource_class      = SaleResource