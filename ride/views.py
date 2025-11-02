from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CurrentTripe, TableTripe
from .Serializer import CurrentTripeSerializer, TableTripeSerializer
from django.shortcuts import render, redirect
from users.models import User
from django.http import JsonResponse
from django.db.models import Q
from .models import DriverQueue, AcceptedTrip, CurrentTripe
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

class CurrentTripeViewSet(viewsets.ModelViewSet):
    queryset = CurrentTripe.objects.all()
    serializer_class = CurrentTripeSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # وقتی درخواست ساخته میشه، همیشه در table_tripe ذخیره‌ش هم کن
        TableTripe.objects.create(
            passenger=instance.passenger,
            request_type=instance.request_type,
            request_time=instance.request_time,
            request_date=instance.request_date,
        )


class TableTripeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TableTripe.objects.all()
    serializer_class = TableTripeSerializer


# صفحه همه کاربرا برای انتخاب
def user_list(request):
    users = User.objects.all()
    return render(request, 'ride/user_list.html', {'users': users})


# فرم ساخت درخواست برای یوزر انتخاب‌شده
def create_tripe(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        request_type = request.POST.get('request_type')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        request_date = request.POST.get('request_date')
        request_time = request.POST.get('request_time')

        # بررسی وجود کاربر و نقش مسافر
        passenger = get_object_or_404(User, id=user_id, role='مسافر')

        # ⛔ کنترل تکرار: اگر سفر فعال دارد
        if CurrentTripe.objects.filter(passenger=passenger, is_active=True, is_completed=False).exists():
            return JsonResponse({'error': 'این مسافر در حال حاضر در سفر است یا سفرش هنوز تمام نشده و نمی‌تواند درخواست جدید ثبت کند.'}, status=400)


        # ✅ ایجاد سفر فعال
        current = CurrentTripe.objects.create(
            passenger=passenger,
            request_type=request_type,
            origin=origin,
            destination=destination,
            request_date=request_date,
            request_time=request_time,
            is_active=True
        )

        # 📝 ثبت در جدول آرشیو
        TableTripe.objects.create(
            passenger=passenger,
            request_type=request_type,
            origin=origin,
            destination=destination,
            request_date=request_date,
            request_time=request_time
        )

        return redirect('current_tripes')

    # اگر متد GET بود، فرم را نمایش بده
    return render(request, 'ride/create_tripe.html')


# لیست درخواست‌های فعال
def current_tripes(request):
    trips = CurrentTripe.objects.all()
    return render(request, 'ride/current_tripes.html', {'trips': trips})


# لیست کل درخواست‌ها (آرشیو)
def table_tripes(request):
    trips = TableTripe.objects.all()
    return render(request, 'ride/table_tripes.html', {'trips': trips})


# پیدا کردن مسافران بر اساس نام برای ساجست دادن
def search_passengers(request):
    query = request.GET.get("q", "").strip()

    passengers = User.objects.filter(
        Q(role="مسافر") &
        (
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(username__icontains=query)
        )
    )

    results = [
        {"id": u.id, "name": u.name, "phone": u.phone}
        for u in passengers
    ]
    return JsonResponse(results, safe=False)


# برای بخش قبول کردن درخاست ها توسط راننده ها از این بخشه 
def join_queue(request):
    if request.method == 'POST':
        zone = request.POST.get('zone')
        driver_id = request.POST.get('driver_id')
        driver = User.objects.get(id=driver_id, role='راننده')

        exists = DriverQueue.objects.filter(driver=driver, is_active=True)
        if exists:
            return render(request, 'ride/join_queue.html', {'error': 'شما همین الان در صف هستید.'})

        DriverQueue.objects.create(driver=driver, zone=zone)
        return redirect('view_queue')
    return render(request, 'ride/join_queue.html')


def view_queue(request):
    city_queue = DriverQueue.objects.filter(zone='city', is_active=True).order_by('joined_at')
    village_queue = DriverQueue.objects.filter(zone='village', is_active=True).order_by('joined_at')

    return render(request, 'ride/view_queue.html', {
        'city_queue': city_queue,
        'village_queue': village_queue,
    })


def view_passenger_requests(request, driver_id):
    driver = User.objects.get(id=driver_id, role='راننده')

    city_queue = DriverQueue.objects.filter(zone='city', is_active=True)
    village_queue = DriverQueue.objects.filter(zone='village', is_active=True)

    # بررسی اینکه راننده نفر اول صف هست
    is_first_city = city_queue.first().driver == driver if city_queue.exists() else False
    is_first_village = village_queue.first().driver == driver if village_queue.exists() else False
    if not (is_first_city or is_first_village):
        return render(request, 'ride/not_allowed.html', {'error': 'فقط نفر اول صف اجازه مشاهده درخواست‌ها را دارد.'})

    trips = CurrentTripe.objects.filter(is_active=True)
    return render(request, 'ride/view_requests.html', {'trips': trips, 'driver': driver})


def view_movements(request):
    movements = AcceptedTrip.objects.all().order_by('-created_at')
    return render(request, 'ride/view_movements.html', {'movements': movements})

# حذف درخواست از صفحه مشاهده درخواست‌ها
def delete_current_tripe(request, tripe_id):
    tripe = get_object_or_404(CurrentTripe, id=tripe_id)
    tripe.delete()
    return redirect('current_tripes')  # برگرد به لیست درخواست‌های فعال


# صفحه اصلی صف راننده
def driver_queue_page(request):
    city_queue = DriverQueue.objects.filter(zone='city', is_active=True).order_by('joined_at')
    village_queue = DriverQueue.objects.filter(zone='village', is_active=True).order_by('joined_at')
    return render(request, 'ride/driver_queue.html', {
        'city_queue': city_queue,
        'village_queue': village_queue,
    })


# سرچ رانندگان برای انتخاب سریع
def search_drivers(request):
    q = request.GET.get('q', '')
    results = User.objects.filter(role='راننده', name__icontains=q)[:10]
    data = [{'id': r.id, 'name': r.name} for r in results]
    return JsonResponse(data, safe=False)


# افزودن راننده به صف شهر یا روستا
def add_driver_to_queue(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        zone = request.POST.get('zone')

        if not driver_id:
            return JsonResponse({'error': 'شناسه راننده ارسال نشده'}, status=400)

        driver = get_object_or_404(User, id=int(driver_id))

        # ⛔ کنترل تکرار: راننده نباید قبلاً در صف فعال باشد
        if DriverQueue.objects.filter(driver=driver, is_active=True, zone=zone).exists():
            return JsonResponse({'error': 'این راننده هم‌اکنون در صف فعال قرار دارد و نمی‌تواند دوباره وارد شود.'}, status=400)

        # ✅ افزودن راننده جدید به صف
        DriverQueue.objects.create(driver=driver, zone=zone, is_active=True)

        return redirect('driver_queue_page')

    # اگر متد GET بود (احتمالاً لازم نیست)
    return render(request, 'ride/driver_queue_page.html')


# تست دسترسی نفر اول به لیست درخواست‌های مسافر
def check_driver_access(request):
    driver_name = request.POST.get('driver_name')
    driver = User.objects.filter(name=driver_name, role='راننده').first()

    if not driver:
        return JsonResponse({'error': 'راننده پیدا نشد'}, status=404)

    city_first = DriverQueue.objects.filter(zone='city', is_active=True).order_by('joined_at').first()
    village_first = DriverQueue.objects.filter(zone='village', is_active=True).order_by('joined_at').first()

    # تشخیص اینکه راننده نفر اول صف کدام منطقه است
    is_first = False
    zone = None
    if city_first and city_first.driver == driver:
        is_first = True
        zone = 'city'
    elif village_first and village_first.driver == driver:
        is_first = True
        zone = 'village'

    if is_first:
        trips = CurrentTripe.objects.filter(is_active=True)
        data = [
            {
                'id': t.id,
                'passenger': t.passenger.name,
                'origin': t.origin,
                'destination': t.destination,
                'type': t.request_type
            }
            for t in trips
        ]

        return JsonResponse({
            'status': 'ok',
            'driver_id': driver.id,    # 🔥 اضافه شد
            'zone': zone,              # 🔥 برای دانستن محدوده صف
            'trips': data
        })

    else:
        return JsonResponse({'status': 'error', 'message': 'دسترسی ندارید'}, status=403)
    
# حذف راننده از صف  
def remove_driver(request, driver_id):
    driver_queue = get_object_or_404(DriverQueue, id=driver_id)
    driver_queue.delete()
    return redirect('driver_queue_page')


# صف راننده‌ها برای قبول کردن درخواست‌ها
@csrf_exempt
def accept_requests(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'روش ارسال اشتباه است (فقط POST مجاز است)'}, status=405)

    driver_id = request.POST.get('driver_id')
    trip_ids = request.POST.getlist('trip_ids')

    if not driver_id or not trip_ids:
        return JsonResponse({'error': 'شناسه راننده یا لیست درخواست‌ها ارسال نشده است'}, status=400)

    # ------------------ بررسی راننده ------------------
    try:
        driver = User.objects.get(id=driver_id, role='راننده')
    except User.DoesNotExist:
        return JsonResponse({'error': 'راننده یافت نشد'}, status=404)

    # ------------------ بررسی صف فعال ------------------
    active_queue = DriverQueue.objects.filter(driver=driver, is_active=True).first()
    if not active_queue:
        return JsonResponse({'error': 'راننده در صف فعال نیست'}, status=403)

    zone = active_queue.zone
    all_drivers = list(DriverQueue.objects.filter(zone=zone, is_active=True).order_by('joined_at'))

    # ------------------ جایگاه راننده ------------------
    try:
        driver_index = all_drivers.index(active_queue)
    except ValueError:
        return JsonResponse({'error': 'خطا در محاسبه جایگاه راننده در صف'}, status=500)

    if driver_index != 0:
        return JsonResponse({'error': 'راننده باید نفر اول صف باشد'}, status=403)

    # ------------------ دریافت درخواست‌های فعال انتخاب‌شده ------------------
    chosen_trips = list(CurrentTripe.objects.filter(id__in=trip_ids, is_active=True))
    if not chosen_trips:
        return JsonResponse({'error': 'هیچ درخواست فعالی یافت نشد'}, status=404)

    # ------------------ تشخیص نوع درخواست ------------------
    types = [trip.request_type for trip in chosen_trips]

    # ---- قوانین پذیرش ----
    if 'vip' in types:
        chosen_trips = [t for t in chosen_trips if t.request_type == 'vip']

    elif 'hurryup' in types:
        chosen_trips = [t for t in chosen_trips if t.request_type == 'hurryup']

    elif all(t.request_type == 'normal' for t in chosen_trips):
        if len(chosen_trips) > 4:
            return JsonResponse({'error': 'حداکثر ۴ درخواست نرمال مجاز است'}, status=400)
        # مجاز است ادامه بده
    else:
        return JsonResponse({'error': 'ترکیب نوع درخواست معتبر نیست'}, status=400)

    # ------------------ ثبت پذیرش نهایی ------------------
    for trip in chosen_trips:
        # ساخت رکورد AcceptedTrip برای هر سفر پذیرفته‌شده
        AcceptedTrip.objects.create(
            current_trip=trip,  # ✅ **اصلاح شد**: اتصال به درخواست اولیه
            driver=driver,
            passenger=trip.passenger,
            request_type=trip.request_type,
            zone=zone
        )

        # غیرفعال شدن سفر در CurrentTripe فقط برای انتخاب‌شده
        trip.is_active = False
        # is_completed را اینجا False نگه می‌داریم تا در پایان سفر True شود
        trip.save(update_fields=['is_active'])

    # خروج راننده از صف
    active_queue.is_active = False
    active_queue.save(update_fields=['is_active'])

    # ------------------ پاسخ موفق ------------------
    return JsonResponse({
        'success': True,
        'accepted_count': len(chosen_trips),
        'zone': zone,
        'types': list(set(types)),
        'message': f"راننده {driver.name} حرکت کرد و {len(chosen_trips)} درخواست پذیرفت."
    })



# مشاهده درخاست صفحه درخاست مسافر قبول کردن
def driver_accept_page(request):
    driver_id = request.GET.get('driver_id')

    if not driver_id:  
        # یعنی هنوز چیزی نفرستادی، فقط فرم رو نشون بده
        return render(request, 'ride/driver_accept_page.html', {
            'driver': None,
            'movements': []
        })

    driver = get_object_or_404(User, id=driver_id, role='راننده')
    movements = AcceptedTrip.objects.filter(driver=driver).order_by('-created_at')

    return render(request, 'ride/driver_accept_page.html', {
        'driver': driver,
        'movements': movements
    })


# حذف درخاست قبول شده
@csrf_exempt
def delete_trip(request, trip_id):
    """
    ✅ **اصلاح کامل شد**: این ویو حالا سفر را از جدول AcceptedTrip حذف می‌کند.
    """
    if request.method == 'POST':
        try:
            # FIX: مدل از CurrentTripe به AcceptedTrip تغییر کرد
            trip = get_object_or_404(AcceptedTrip, id=trip_id)
            trip.delete()
            return JsonResponse({'status': 'deleted'})
        except AcceptedTrip.DoesNotExist:
            return JsonResponse({'error': 'سفر پذیرفته‌شده یافت نشد.'}, status=404)
    return JsonResponse({'error': 'متد نامعتبر'}, status=405)


# پایاین سفر توسط راننده
@csrf_exempt
def finish_trip(request, trip_id):
    """
    راننده پایان سفر را اعلام می‌کند
    ✅ **اصلاح شد**: آپدیت مسافر حالا دقیق و ایمن است.
    """
    try:
        trip = AcceptedTrip.objects.get(id=trip_id)
    except AcceptedTrip.DoesNotExist:
        return JsonResponse({'error': 'سفر یافت نشد'}, status=404)

    # ۱. علامت‌گذاری سفر به‌عنوان انجام‌شده
    trip.is_finished = True
    trip.save(update_fields=['is_finished'])

    # ۲. راننده دوباره فعال می‌شود
    driver_queue, _ = DriverQueue.objects.get_or_create(driver=trip.driver, zone=trip.zone)
    driver_queue.is_active = True
    driver_queue.save()

    # ۳. ✅ مسافر دوباره اجازه درخواست سفر دارد (به‌صورت دقیق)
    if trip.current_trip:
        original_trip = trip.current_trip
        original_trip.is_completed = True
        original_trip.save(update_fields=['is_completed'])

    return JsonResponse({'success': True, 'message': 'سفر با موفقیت به پایان رسید.'})

