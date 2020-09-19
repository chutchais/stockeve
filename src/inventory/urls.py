"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

from api.base.router import api_urlpatterns as api_v1

urlpatterns = [
	path('',views.index ,name='index'),
    # API path
    path('api/v1/', include(api_v1)),

    path('about/',views.about, name='about'),
    path('promotion/',include(('promotion.urls','promotion'), namespace='promotion')),
    path('contact/',views.contact, name='contact'),
    path('login/',views.home ,name='home'),
    path('admin/', admin.site.urls),
    path('product/',include(('product.urls','product'),namespace='product')),
    path('sale/',include(('sale.urls','sale'),namespace='sale')),
    path('receiving/',include(('receiving.urls','receiving'),namespace='receiving')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('auth/change_password_done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), 
        name='change_password_done'),
    path('auth/change_password/', 
        auth_views.PasswordChangeView.as_view(template_name='auth/password_change_form.html',
        success_url='/auth/change_password_done/'), 
        name='change_password'),
    # Added by Chutchai on Apr 26,2020 -- To support Reset Password feature.
    path('auth/password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html',
        success_url='done/'), 
        name="password_reset"),
    path('auth/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), 
        name="password_reset_done"),
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html',
        success_url='/auth/reset/done/'),
        name="password_reset_confirm"),
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), 
        name="password_reset_complete"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Siam Manor - Inventory Management system'
admin.site.site_title = "Inventory Management Admin"
admin.site.index_title = "Welcome to Inventory Management system"