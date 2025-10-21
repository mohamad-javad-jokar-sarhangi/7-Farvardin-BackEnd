from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views

from .views import (
    CreateTripView,
    request_form_page,
    queue_status_page,
    TripRequestViewSet,
    accept_trip_request,
)

# Router برای APIها
router = DefaultRouter()
router.register(r'trip-requests', TripRequestViewSet, basename='triprequest')

urlpatterns = [
    # API
    path('trip/create/', CreateTripView.as_view(), name='create-trip'),

    # HTML
    path('request-form/', request_form_page, name='request_form'),
    path('queue-status/', queue_status_page, name='queue_status'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    
    # API Router endpointها
    path('', include(router.urls)),  # ← این خط اجازه می‌دهد مسیرهای CRUD کار کنند
    
    
    path('accept-trip/', accept_trip_request, name='accept_trip'),
]
