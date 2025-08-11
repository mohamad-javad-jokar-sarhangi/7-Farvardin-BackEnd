from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import RideRequest, DriverQueue
from .Serializer import RideRequestSerializer


class DriverRideRequestListView(generics.ListAPIView):
    serializer_class = RideRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not getattr(user, 'is_driver', False):
            return RideRequest.objects.none()

        # درخواست‌های شب قبل → همه راننده‌ها می‌بینند
        scheduled = RideRequest.objects.filter(
            status='pending', request_type='scheduled'
        )

        # درخواست‌های عادی → فقط اگر راننده نفر اول صف باشد
        normal_requests = []
        queues = DriverQueue.objects.filter(driver=user, position=1)
        for q in queues:
            qs = RideRequest.objects.filter(
                status='pending',
                request_type='normal',
                origin=q.location
            ) | RideRequest.objects.filter(
                status='pending',
                request_type='normal',
                destination=q.location
            )
            normal_requests.extend(list(qs))

        return (
            scheduled | RideRequest.objects.filter(id__in=[r.id for r in normal_requests])
        ).distinct()


class AcceptRideRequestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        ride_request = get_object_or_404(RideRequest, id=pk, status='pending')

        # بررسی مجاز بودن
        if ride_request.request_type == 'scheduled':
            pass  # همه راننده‌ها مجازند
        elif ride_request.request_type == 'normal':
            in_queue_first = DriverQueue.objects.filter(
                driver=user, position=1
            ).filter(location__in=[ride_request.origin, ride_request.destination]).exists()
            if not in_queue_first:
                return Response({'detail': 'شما مجاز به پذیرش این درخواست نیستید'}, status=403)

        # تغییر وضعیت و ثبت راننده
        ride_request.driver = user
        ride_request.status = 'accepted'
        ride_request.save()

        # اگر درخواست عادی بود → حذف راننده از صف مربوطه
        if ride_request.request_type == 'normal':
            DriverQueue.objects.filter(
                driver=user, location__in=[ride_request.origin, ride_request.destination]
            ).delete()

        return Response({'detail': 'درخواست با موفقیت تایید شد'})
