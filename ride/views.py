from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from .models import TripRequest, DriverQueue, DriverAcceptance
from .Serializer import TripRequestSerializer, DriverQueueSerializer, DriverAcceptanceSerializer

# مسافر درخواست می‌دهد
class CreateTripView(generics.CreateAPIView):
    serializer_class = TripRequestSerializer


# راننده وارد صف می‌شود
class JoinDriverQueueView(generics.CreateAPIView):
    serializer_class = DriverQueueSerializer


# پذیرش سفر بر اساس اولویت صف‌ها
class AcceptTripView(generics.CreateAPIView):
    serializer_class = DriverAcceptanceSerializer

    def create(self, request, *args, **kwargs):
        trip_id = request.data.get("trip_request")
        driver_id = request.data.get("driver")
        last_village_name = "آخرین روستا"  # یا از config بخونیم
        city_name = "شهر"

        trip = get_object_or_404(TripRequest, id=trip_id)

        # اول صف راننده‌های آخرین روستا
        first_village_driver = DriverQueue.objects.filter(
            queue_type='village',
            location_name=last_village_name
        ).order_by('position', 'joined_at').first()

        # پذیرش
        if first_village_driver and first_village_driver.driver.id == driver_id:
            trip.status = 'accepted'
            trip.save()
            DriverAcceptance.objects.create(driver_id=driver_id, trip_request=trip)
            first_village_driver.delete()
            return Response({"message": "سفر از صف روستا پذیرفته شد"}, status=status.HTTP_201_CREATED)

        # اگر روستا خالی → نفر اول صف شهر
        if not first_village_driver:
            first_city_driver = DriverQueue.objects.filter(
                queue_type='city',
                location_name=city_name
            ).order_by('position', 'joined_at').first()
            if first_city_driver and first_city_driver.driver.id == driver_id:
                trip.status = 'accepted'
                trip.save()
                DriverAcceptance.objects.create(driver_id=driver_id, trip_request=trip)
                first_city_driver.delete()
                return Response({"message": "سفر از صف شهر پذیرفته شد"}, status=status.HTTP_201_CREATED)

        return Response({"message": "شما نفر اول صف مجاز نیستید"}, status=status.HTTP_400_BAD_REQUEST)


# صفحات HTML ساده

def request_form_page(request):
    message = None
    if request.method == "POST":
        TripRequest.objects.create(
            passenger=request.user,
            origin=request.POST.get("origin"),
            destination=request.POST.get("destination")
        )
        message = "درخواست ثبت شد."
    return render(request, "ride/request_form.html", {"message": message})



def queue_status_page(request):
    trips = TripRequest.objects.all()
    return render(request, "ride/queue_status.html", {"trips": trips})
