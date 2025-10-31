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
    #
    

]
