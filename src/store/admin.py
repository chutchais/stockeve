from django.contrib import admin

# Register your models here.
from .models import Store

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

class StoreResource(resources.ModelResource):
    class Meta:
        model = Store
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped= True
        exclude = ('user','created','updated' )

@admin.register(Store)
class StoreAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','title']
	# list_filter = []
	list_display = ('name','title','incoming','sale_able',
						'total_product','created','status')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user','total_product')
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','title','incoming','sale_able','status']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	resource_class      = StoreResource
	

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(StoreAdmin, self).save_model(request, obj, form, change)

