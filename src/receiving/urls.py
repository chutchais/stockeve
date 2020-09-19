from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from .views import (ReceivingListView,
					ReceivingDetailView)


urlpatterns = [
	# Page
	path('',ReceivingListView.as_view(),name='list'),
    path('<pk>',ReceivingDetailView.as_view(),name='detail'),
]