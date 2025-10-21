from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from .models import TripRequest , DriverQueue
from .Serializer import TripRequestSerializer , DriverQueueSerializer
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


class DriverQueueViewSet(viewsets.ModelViewSet):
    queryset = DriverQueue.objects.all().order_by('joined_at')
    serializer_class = DriverQueueSerializer

    def create(self, request, *args, **kwargs):
        driver_id = request.data.get('driver')
        direction = request.data.get('direction')
        print('DEBUG POST DATA:', request.data)  # 👈 اضافه کن

        # 👇 چک تکراری بودن در صف فعال
        if DriverQueue.objects.filter(driver_id=driver_id, direction=direction, is_active=True).exists():
            return Response({"detail": "❌ این راننده در حال حاضر در صف همین مسیر است."}, status=400)

        return super().create(request, *args, **kwargs)


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
    print('DEBUG DIRECTION:', direction)
    try:
        trip_id = request.data.get('trip_id')
        driver_id = request.data.get('driver_id')
        direction = request.data.get('direction') or request.GET.get('direction')

        with transaction.atomic():
            first_driver = (DriverQueue.objects
                            .filter(direction=direction, is_active=True)
                            .order_by('joined_at')
                            .select_for_update()
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


@api_view(['GET'])
def get_driver_queue(request):
    """
    دریافت صف رانندگان بر اساس جهت حرکت
    """
    direction = request.GET.get('direction')
    if not direction:
        return Response({'detail': 'پارامتر direction الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)

    queue = (
        DriverQueue.objects
        .filter(direction=direction)
        .order_by('joined_at')
        .select_related('driver')
    )

    data = []
    for idx, q in enumerate(queue, start=1):
        data.append({
            'position': idx,                    # شماره صف
            'driver_id': q.driver.id,           # شناسه راننده
            'driver_name': q.driver.username,   # نام کاربری راننده
            'direction': q.direction,           # سمت حرکت برای اطمینان
            'is_active': q.is_active,           # فعال بودن یا نه
            'joined_at': q.joined_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return Response({'queue': data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_driver_queue(request):
    """
    ریست کامل صف رانندگان
    """
    deleted_count, _ = DriverQueue.objects.all().delete()
    return Response(
        {'detail': f'✅ صف رانندگان ریست شد ({deleted_count} رکورد حذف شد).'},
        status=status.HTTP_200_OK
    )



def driver_console(request):
    return render(request, 'ride/driver_console.html')

@api_view(['GET'])
def search_drivers(request):
      q = request.GET.get('q', '')
      drivers = User.objects.filter(role='راننده', username__icontains=q)[:10]
      data = [{'id': d.id, 'username': d.username} for d in drivers]
      return Response(data)


# ride/views.py
@api_view(['POST'])
def reset_driver_queue(request):
    DriverQueue.objects.all().delete()
    return Response({'detail': 'صف رانندگان ریست شد.'})
