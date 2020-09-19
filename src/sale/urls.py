from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from .views import (SaleListView,export_sale_child_xls)


urlpatterns = [
	# Page
	path('report/child/',export_sale_child_xls, name='export_sale_child_xls'),
	path('',SaleListView.as_view(),name='list'),
   
]