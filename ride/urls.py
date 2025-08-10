from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ride.views import TripRequestViewSet
from . import views


router = DefaultRouter()
router.register(r'rides', TripRequestViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('requests/', views.ride_requests_list, name='ride_requests_list'),
    path('passenger-suggestions/', views.passenger_name_suggestions, name='passenger_name_suggestions'),
]