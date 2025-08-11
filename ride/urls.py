from django.urls import path
from .views import DriverRideRequestListView, AcceptRideRequestView


urlpatterns = [
    path('driver/requests/', DriverRideRequestListView.as_view(), name='driver-requests'),
    path('driver/requests/<int:pk>/accept/', AcceptRideRequestView.as_view(), name='accept-ride'),
]
