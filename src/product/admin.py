from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Brand,Product,ProductFamily,ProductSubFamily,ProductStock,ProductImage

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

# # Register your models here.
from import_export.fields import Field
class ProductResource(resources.ModelResource):
	total_qty = Field(attribute='total_qty',readonly =True)
	class Meta:
		model = Product
		import_id_fields = ('number',)
		fields = ('number','title','description','childs','brand','subfamily','finished_goods','total_qty',
				'min_stock','max_stock','lower_stock','higher_stock','unit_name','note','status')
		export_order = ('number','title','description','childs','brand','subfamily','finished_goods','total_qty',
				'min_stock','max_stock','lower_stock','higher_stock','unit_name','note','status')
		skip_unchanged = True
		report_skipped= True
		exclude = ('user','created','updated' )

# class ProductInline(admin.TabularInline):
# 	model 				= Product
# 	fields 				= ('number','title','total_qty')
# 	extra 				= 0
# 	show_change_link 	= True
# 	readonly_fields 	= ['total_qty']
# 	can_delete 			= False
# 	# autocomplete_fields = ['number']
# 	verbose_name 		= 'Child Product detail'
# 	verbose_name_plural = 'Child Product detail'

# class SubProductInlineFormset(generic.generic_inlineformset_factory(Product)):
#     def __init__(self, *args, **kwargs):
#         super(SubProductInlineFormset, self).__init__(*args, **kwargs)
#         self.can_delete = False

class ProductStockInline(admin.TabularInline):
	model = ProductStock
	fields = ('store','qty','note','updated')
	readonly_fields = ('created','updated','user')
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	show_change_link = True
	verbose_name = 'Stock detail'
	verbose_name_plural = 'Stock detail'

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	fields = ('file','note','updated')
	readonly_fields = ('created','updated')
	extra = 0 # how many rows to show
	# autocomplete_fields = ('operation','next_pass','next_fail')
	show_change_link = True
	verbose_name = 'Image detail'
	verbose_name_plural = 'Image detail'

@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','title']
	# list_filter = []
	list_display = ('name','title','created','status')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','title','status']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(BrandAdmin, self).save_model(request, obj, form, change)

@admin.register(ProductFamily)
class ProductFamilyAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','title']
	# list_filter = []
	list_display = ('name','title','created','status')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','title','status']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(ProductFamilyAdmin, self).save_model(request, obj, form, change)

@admin.register(ProductSubFamily)
class ProductSubFamilyAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','title']
	# list_filter = []
	list_display = ('name','family','title','total_product','created','status')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','family','title','status']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(ProductSubFamilyAdmin, self).save_model(request, obj, form, change)
# admin.site.register(ProductFamily,ProductFamilyAdmin)
# class IsLowerMinStockFilter(admin.SimpleListFilter):
#     title = 'is_lower_stock'
#     parameter_name = 'is_lower_stock'

#     def lookups(self, request, model_admin):
#         return (
#             ('Yes', 'Yes'),
#             ('No', 'No'),
#         )

#     def queryset(self, request, queryset):
#         value = self.value()
#         if value == 'Yes':
#             return queryset.filter(stocks__gt=10)
#         elif value == 'No':
#             return queryset.exclude(stocks__gt=10)
#         return queryset

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['number','title','description']
	list_filter = ['finished_goods','lower_stock','higher_stock','unit_name','brand','subfamily__family']
	list_display = ('number','title','is_sets','finished_goods','brand','total_qty','total_unsale_qty','min_stock','max_stock',
					'lower_stock','higher_stock')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user','total_qty','total_unsale_qty')
# 'lower_stock','higher_stock',
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True
	filter_horizontal = ('childs',)

	fieldsets = [
		('Basic Information',{'fields': ['number','title','brand','description','subfamily','finished_goods','status']}),
		('Available Stock',{'fields': [('total_qty','total_unsale_qty'),('min_stock','lower_stock'),
								('max_stock','higher_stock'),]}),
		('Parent Product',{'fields': ['childs']}),
		('Note',{'fields': ['note']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	inlines =[ProductStockInline,ProductImageInline]
	resource_class      = ProductResource

	def is_lower_min_stock(self, obj):
		return int(obj.total_qty) < obj.min_stock
	is_lower_min_stock.boolean = True

	def is_sets(self,obj):
		return True if obj.childs.count() > 0 else False
	is_sets.boolean = True

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(ProductAdmin, self).save_model(request, obj, form, change)


@admin.register(ProductStock)
class ProductStockAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['product__number','product__title']
	list_filter = ['store']
	list_display = ('product','store','qty','updated','status')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')

	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	# fieldsets = [
	# 	('Basic Information',{'fields': ['number','title','brand','description','subfamily','status']}),
	# 	('Available Stock',{'fields': [('total_qty','total_unsale_qty'),'min_stock','max_stock','lower_stock']}),
	# 	('Parent Product',{'fields': ['parent']}),
	# 	('Note',{'fields': ['note']}),
	# 	('System Information',{'fields':[('user','created'),'updated']})
	# ]


# class FriendAdmin(admin.ModelAdmin):
#     filter_horizontal = ('friends',)

# admin.site.register(Person,FriendAdmin)