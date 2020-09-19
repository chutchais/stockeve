from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from .views import (ProductDetailView,
					ProductListView,
					ProductStockListView,ProductStockDetailView)


urlpatterns = [
	# Page
	path('stock',ProductStockListView.as_view(),name='stock-list'),
	path('stock/<pk>',ProductStockDetailView.as_view(),name='stock-detail'),
	path('',ProductListView.as_view(),name='list'),
    path('<pk>',ProductDetailView.as_view(),name='detail'),
    
]