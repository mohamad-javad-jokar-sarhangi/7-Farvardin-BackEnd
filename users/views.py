from .forms import UserNotRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserNotRegister, User



def home_view(request):
    return render(request, 'home.html')  # رندر کردن فایل home.html

# ثبت‌نام کاربر جدید
def signup_view(request):
    if request.method == 'POST':
        form = UserNotRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/signup_success.html')  # موفقیت در ثبت‌نام
    else:
        form = UserNotRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

# نمایش کاربران ثبت‌نشده
def unregistered_users_view(request):
    users = UserNotRegister.objects.all()  # دریافت همه کاربران ثبت‌نشده
    context = {'users': users}
    return render(request, 'users/unregistered_users.html', context)

# تأیید کاربر توسط ادمین
def approve_user(request, user_id):
    user = get_object_or_404(UserNotRegister, id=user_id)  # دریافت کاربر ثبت‌نشده
    User.objects.create(name=user.name, phone=user.phone, role=user.role)
    user.delete()  # حذف از لیست کاربران ثبت‌نشده
    return redirect('unregistered_users')  # بازگشت به صفحه کاربران ثبت‌نشده

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
