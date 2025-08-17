from rest_framework import viewsets
from .models import TripRequest
from .Serializer import TripRequestSerializer 
from django.shortcuts import render
from .models import TripRequest
from django.db.models import Q
from users.models import User

class TripRequestViewSet(viewsets.ModelViewSet):
    queryset = TripRequest.objects.all().order_by('-created_at')
    serializer_class = TripRequestSerializer


def ride_requests_list(request):
    query_name = request.GET.get('passenger_name', '')
    query_start_date = request.GET.get('start_date', '')
    query_end_date = request.GET.get('end_date', '')

    trip_requests = TripRequest.objects.all().order_by('-created_at')

    # فیلتر بر اساس نام مسافر
    if query_name:
        trip_requests = trip_requests.filter(passenger__name__icontains=query_name)

    # فیلتر تاریخ
    if query_start_date:
        trip_requests = trip_requests.filter(created_at__date__gte=query_start_date)
    if query_end_date:
        trip_requests = trip_requests.filter(created_at__date__lte=query_end_date)

    context = {
        'trip_requests': trip_requests,
        'passenger_name': query_name,
        'start_date': query_start_date,
        'end_date': query_end_date,
    }
    return render(request, 'ride/ride_requests_list.html', context)


# این ویو برای پیشنهاد نام مسافر (AJAX)
from django.http import JsonResponse

def passenger_name_suggestions(request):
    term = request.GET.get('term', '')
    suggestions = list(User.objects.filter(name__icontains=term).values_list('name', flat=True)[:10])
    return JsonResponse(suggestions, safe=False)
