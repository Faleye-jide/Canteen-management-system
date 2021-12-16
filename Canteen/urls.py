"""Canteen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Customer.views import index, About, contact, Order, menuView, searchMenu, login, register, logout, MY_ORDERS
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
admin.site.site_header = "Restaurant System Admin"
admin.site.site_title = "Restaurant System Admin"
admin.site.index_title = "Restaurant System Administration"



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('contact/',contact.as_view(), name='contact'),
    path('order/',Order.as_view(), name='order'),
    path('menu/',menuView.as_view(), name='menu'),
    path('menu/search',searchMenu.as_view(), name='search'),
    path('login/',login,name='login'),
    path('register/',register, name='register'),
    path('logout/',register, name='logout'),
    path('my_orders/',MY_ORDERS.as_view(), name='my_orders'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
