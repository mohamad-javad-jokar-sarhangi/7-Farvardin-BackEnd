from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from .models import TripRequest , DriverQueue
from .Serializer import TripRequestSerializer
from users.models import User
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction

# مسافر درخواست می‌دهد
class CreateTripView(generics.CreateAPIView):
    serializer_class = TripRequestSerializer

class TripRequestViewSet(viewsets.ModelViewSet):
    queryset = TripRequest.objects.all()
    serializer_class = TripRequestSerializer

# ایجاد درخاست ماشین
def request_form_page(request):
    message = None
    if request.method == "POST":
        default_passenger = User.objects.first()  # برای تست بدون لاگین

        TripRequest.objects.create(
            passenger_name=request.POST.get("passenger_name"),   # گرفتن نام مسافر
            passenger_phone=request.POST.get("passenger_phone"), # گرفتن شماره تماس
            origin=request.POST.get("origin"),
            destination=request.POST.get("destination"),
            request_type=request.POST.get("request_type")  # اگه تو فرم داری
        )

        message = "درخواست ثبت شد."

    return render(request, "ride/request_form.html", {"message": message})


# مشاده درخاست خای ماشین 
def queue_status_page(request):
    trips = TripRequest.objects.all()
    return render(request, "ride/queue_status.html", {"trips": trips})


# پاک کردن درخاست های ماشین 
def delete_trip(request, trip_id):
    trip = get_object_or_404(TripRequest, id=trip_id)
    trip.delete()
    return redirect('queue_status')


# درخواست سفر را راننده اول صف قبول می‌کند
@api_view(['POST'])
def accept_trip_request(request):
    try:
        trip_id = request.data.get('trip_id')
        driver_id = request.data.get('driver_id')
        direction = request.data.get('direction')

        with transaction.atomic():
            first_driver = (DriverQueue.objects
                            .select_for_update()
                            .filter(direction=direction, is_active=True)
                            .order_by('joined_at')
                            .first())

            if not first_driver or first_driver.driver.id != int(driver_id):
                return Response({'detail': 'فقط نفر اول صف مجاز به پذیرش است.'}, status=status.HTTP_403_FORBIDDEN)

            trip = TripRequest.objects.select_for_update().get(id=trip_id)
            trip.accepted_by_id = driver_id
            trip.save()

            first_driver.is_active = False
            first_driver.save()

            # ✅ اینجا باید اضافه شود
            next_driver = (DriverQueue.objects
                           .filter(direction=direction, is_active=True)
                           .order_by('joined_at')
                           .first())
            if next_driver:
                pass  # نفر بعدی خودبه‌خود فعال است؛ نیازی به تغییر نیست

        return Response({'detail': 'درخواست با موفقیت پذیرفته شد.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'detail': f'خطا: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


