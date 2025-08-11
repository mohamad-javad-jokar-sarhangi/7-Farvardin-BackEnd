"""
URL configuration for Nighbarhood_BackEnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path , include
from users.views import home_view
from rest_framework.routers import DefaultRouter
from ride.views import DriverRideRequestListView, AcceptRideRequestView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('users/', include('users.urls')), 
    path('articles/', include('article.urls')),
    path('articles/', include('article.urls')),
    
    # API های راننده
    path('api/driver/requests/', DriverRideRequestListView.as_view(), name='driver-requests'),
    path('api/driver/requests/<int:pk>/accept/', AcceptRideRequestView.as_view(), name='accept-ride'),
]
