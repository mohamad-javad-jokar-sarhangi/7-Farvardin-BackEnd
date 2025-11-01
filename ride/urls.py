from django.urls import path
from . import views

urlpatterns = [
    # ساخت درخواست جدید
    path('create-tripe/', views.create_tripe, name='create_tripe'),
    # لیست درخواست های جاری
    path('current-tripes/', views.current_tripes, name='current_tripes'),
    # لیست همه درخواست‌ها در جدول    
    path('table-tripes/', views.table_tripes, name='table_tripes'),
    # برای پیدا کردن اسم مسافر 
    path("search-passengers/", views.search_passengers, name="search_passengers"),
    # برای حذف درخاست د صفحه مشاهده در خاست ها 
    path('delete-current-tripe/<int:tripe_id>/', views.delete_current_tripe, name='delete_current_tripe'),
    # برای بخش قبول کردن درخواست‌ها
    path('join-queue/', views.join_queue, name='join_queue'),
    path('view-queue/', views.view_queue, name='view_queue'),
    path('driver/<int:driver_id>/requests/', views.view_passenger_requests, name='view_passenger_requests'),
    path('accept-requests/', views.accept_requests, name='accept_requests'),
    path('movements/', views.view_movements, name='view_movements'),
    #
    path('driver-queue/', views.driver_queue_page, name='driver_queue_page'),
    path('search-drivers/', views.search_drivers, name='search_drivers'),
    path('add-driver-to-queue/', views.add_driver_to_queue, name='add_driver_to_queue'),
    path('check-access/', views.check_driver_access, name='check_driver_access'),
    
    # حذف راننده از صف
    path('remove-driver/<int:driver_id>/', views.remove_driver, name='remove_driver'),



]
