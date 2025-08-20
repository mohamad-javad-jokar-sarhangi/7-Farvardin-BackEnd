from django.urls import path
from . import views

from .views import (
    CreateTripView, JoinDriverQueueView, AcceptTripView,
    request_form_page, queue_status_page
)

urlpatterns = [
    # API
    path('trip/create/', CreateTripView.as_view(), name='create-trip'),
    path('driver/join-queue/', JoinDriverQueueView.as_view(), name='join-driver-queue'),
    path('driver/accept-trip/', AcceptTripView.as_view(), name='accept-trip'),

    # HTML
    path('request-form/', request_form_page, name='request_form'),
    path('queue-status/', queue_status_page, name='queue_status'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
]
