from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Receiving,Inspection,PoInvHD,PoInvDT
from store.models import Store

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

# # Register your models here.
from product.models import Product,ProductStock
from store.models import Store

class ReceivingResource(resources.ModelResource):
	class Meta:
		model = Receiving
		import_id_fields = ()
		skip_unchanged = True
		report_skipped= True
		exclude = ('id','user','productstock','created','updated','inspected' )
	# def import_obj(self, obj, data, dry_run):
	# 	product = Product.objects.get(number=data.get('product'))
	# 	store   = Store.objects.get(name=data.get('store'))
	# 	print('Input ',product,store)
	# 	obj, created = ProductStock.objects.get_or_create(
	# 		    store = store,
	# 		    product=product
	# 		)
	# 	# if created:
	# 	# # if field.column_name == 'productstock':
	# 	# 	data.update({'productstock':obj })
	# 	# for field in self.get_fields():
	# 	# 	print(data.get('product'),data.get('store'))
	# 	# pass
	# 	self.import_field(field, obj, data)

class InspectionInline(admin.TabularInline):
	model = Inspection
	fields = ('qty','passed','store','note')
	readonly_fields = ('created','updated','user')
	extra = 0 # how many rows to show
	# autocomplete_fields = ('operation','next_pass','next_fail')
	show_change_link = True
	verbose_name = 'Inspection detail'
	verbose_name_plural = 'Inspection detail'


@admin.register(Receiving)
class ReceivingAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['store__name','product__number','description']
	list_filter = ['inspected','status','store']
	list_display = ('product','store','qty','inspected','total_inspect','status','receivedate')
	# list_editable = ('color','move_performa')
	autocomplete_fields = ['product']
	readonly_fields = ('created','updated','user')

	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['product','store','qty','description','status','receivedate']}),
		('Inspection Completed',{'fields': ['inspected']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	inlines 			=[InspectionInline]
	resource_class      = ReceivingResource

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(ReceivingAdmin, self).save_model(request, obj, form, change)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		# Edit on Sep 24,2020 -- To show all Stock
		# if db_field.name == 'store':
		# 	kwargs["queryset"] = Store.objects.filter(incoming = True)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderDetailInline(admin.TabularInline):
	model = PoInvDT
	fields = ('listno','goodcode','goodname','goodqty','goodamnt','invecode')
	readonly_fields = ('listno','goodcode','goodname','goodqty','goodamnt','invecode')
	extra = 0 # how many rows to show

@admin.register(PoInvHD)
class PoInvHDAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['poinvid','docuno']
	# list_filter = [SaleAllProductDateFilter]
	list_display = ('poinvid','docuno','totabaseamnt','vatamnt','netamnt','receivedate','executed')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['product']
	readonly_fields = ('created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True
	ordering = ['-receivedate','poinvid']

	fieldsets = [
		('Basic Information',{'fields': ['poinvid','docuno','receivedate','executed']}),
		('Price',{'fields': ['totabaseamnt','vatamnt','netamnt']}),
		('Vendor',{'fields': ['vendorname']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	# resource_class      = SaleResource
	inlines =[OrderDetailInline]

@admin.register(PoInvDT)
class PoInvDTAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['poinvid__poinvid','poinvid__docuno','goodcode','goodname']
	list_filter = ['invecode']#SaleAllProductDateFilter]
	list_display = ('poinvid','listno','goodcode','goodname','goodqty','goodamnt','invecode','executed')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['product']
	readonly_fields = ('updated','user','created')
	ordering = ['-created','poinvid','listno']

	fieldsets = [
		('Basic Information',{'fields': ['poinvid','listno','goodid','goodcode','goodname','executed']}),
		('Price',{'fields': ['goodqty','goodamnt','inveid','invecode','invename']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
