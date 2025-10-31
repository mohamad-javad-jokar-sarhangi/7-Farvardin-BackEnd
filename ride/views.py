from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CurrentTripe, TableTripe
from .Serializer import CurrentTripeSerializer, TableTripeSerializer
from django.shortcuts import render, redirect
from users.models import User
from django.http import JsonResponse
from django.db.models import Q

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

        # اعتبارسنجی: مطمئن شو فقط مسافرها انتخاب می‌شن
        passenger = User.objects.get(id=user_id, role='مسافر')

        current = CurrentTripe.objects.create(
            passenger=passenger,
            request_type=request_type
        )

        TableTripe.objects.create(
            passenger=passenger,
            request_type=request_type,
            request_time=current.request_time,
            request_date=current.request_date
        )

        return redirect('current_tripes')

    # برای GET، فقط فرم خالی رو نشون بده (JS autocomplete خودش داده رو می‌گیره)
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
