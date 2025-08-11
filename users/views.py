from .forms import UserNotRegisterForm , UserApproveForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserNotRegister, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserNotRegisterSerializer
from .serializers import UserSerializer
from .forms import UserForm
from django.http import JsonResponse

# API
# View برای ثبت‌نام UserNotRegister api
class UserNotRegisterCreateAPIView(APIView):

    def post(self, request):
        serializer = UserNotRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ذخیره داده‌ها در دیتابیس
            return Response({'message': 'User added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserSearchAPIView(APIView):        
    def get(self, request, phone_number):
        try:
            user = User.objects.get(phone=phone_number)
            serializer = UserSerializer(user)
            return JsonResponse(
                serializer.data,
                json_dumps_params={'ensure_ascii': False},
                safe=False
            )
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "کاربر تایید نشده"},
                json_dumps_params={'ensure_ascii': False},
                status=404
            )

# For Panel Admin-------------------------------------------------------------------------------------
def home_view(request):
    return render(request, 'home.html')  # رندر کردن فایل home.html

# ثبت‌نام کاربر جدید
def signup_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/signup_success.html')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})


# نمایش کاربران ثبت‌نشده
def unregistered_users_view(request):
    users = UserNotRegister.objects.all()  # دریافت همه کاربران ثبت‌نشده
    context = {'users': users}
    return render(request, 'users/unregistered_users.html', context)

# تأیید کاربر توسط ادمین
def approve_user(request, user_id):
    user_not_registered = get_object_or_404(UserNotRegister, id=user_id)  # دریافت کاربر ثبت‌نشده
    if request.method == 'POST':
        form = UserApproveForm(request.POST)
        if form.is_valid():
            # اطلاعات کاربر ثبت‌شده نهایی را ذخیره کنیم
            User.objects.create(
                name=user_not_registered.name,
                phone=user_not_registered.phone,
                role=user_not_registered.role,
                location=user_not_registered.location,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            user_not_registered.delete()  # حذف کاربر از لیست ثبت‌نشده
            return redirect('unregistered_users')  # بازگشت به لیست کاربران ثبت‌نشده
    else:
        form = UserApproveForm(initial={
            'name': user_not_registered.name,
            'phone': user_not_registered.phone,
            'role': user_not_registered.role,
            'location': user_not_registered.location,
        })
    return render(request, 'users/approve_user.html', {'form': form})

# رد کردن کاربر توسط ادمین
def reject_user(request, user_id):
    user = get_object_or_404(UserNotRegister, id=user_id)  # دریافت کاربر ثبت‌نشده
    user.delete()  # حذف از لیست کاربران ثبت‌نشده
    return redirect('unregistered_users')  # بازگشت به صفحه کاربران ثبت‌نشده

# نمایش لیست کاربران تأیید‌شده
def registered_users_view(request):
    users = User.objects.all()  # دریافت همه کاربران تأیید‌شده
    context = {'users': users}
    return render(request, 'users/registered_users.html', context)

# حذف کاربر
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)  # دریافت کاربر تأیید‌شده
        user.delete()  # حذف کاربر از دیتابیس
    return redirect('registered_users')  # بازگشت به صفحه کاربران تأیید‌شده

# سرچ با شماره تماس
def search_user_view(request):
    search_attempted = False
    user = None
    
    if 'phone' in request.GET:
        search_attempted = True
        phone_number = request.GET.get('phone')
        try:
            user = User.objects.get(phone=phone_number)
        except User.DoesNotExist:
            user = None
    
    context = {
        'user': user,
        'search_attempted': search_attempted
    }
    
    return render(request, 'users/user_search.html', context)

# search by username password
class UserLoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # بررسی وجود کاربر با username و password
        try:
            user = User.objects.get(username=username, password=password)
            return Response({'exists': True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)


# views.py
def create_user_direct_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/signup_success.html')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

