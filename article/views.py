from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from users.models import User  # مدل User سفارشی

def article_list(request):
    """نمایش لیست تمام مقالات"""
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'article/article_list.html', {'articles': articles})

def article_detail(request, pk):
    """نمایش جزئیات یک مقاله"""
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article/article_detail.html', {'article': article})

def create_article(request):
    """ایجاد مقاله جدید"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_id = request.POST.get('author_id')
        
        # بررسی اعتبار داده‌ها
        if not title or not content:
            users = User.objects.all()
            error_message = "لطفاً عنوان و محتوای مقاله را وارد کنید."
            return render(request, 'article/create_article.html', {
                'users': users,
                'error_message': error_message,
                'title': title,
                'content': content
            })
        
        # تعیین نام نویسنده
        if author_id == 'custom':
            # اگر "نویسنده دیگر" انتخاب شده باشد
            author_name = request.POST.get('custom_author_name')
            if not author_name:
                users = User.objects.all()
                error_message = "لطفاً نام نویسنده را وارد کنید."
                return render(request, 'article/create_article.html', {
                    'users': users,
                    'error_message': error_message,
                    'title': title,
                    'content': content
                })
        else:
            try:
                # پیدا کردن کاربر با شناسه مورد نظر و استفاده از نام او
                author = User.objects.get(id=author_id)
                author_name = author.name  # یا هر فیلدی که نام کاربر در آن ذخیره می‌شود
            except User.DoesNotExist:
                users = User.objects.all()
                error_message = "کاربر انتخاب شده وجود ندارد."
                return render(request, 'article/create_article.html', {
                    'users': users,
                    'error_message': error_message,
                    'title': title,
                    'content': content
                })
        
        article = Article.objects.create(
            title=title,
            content=content,
            author_name=author_name
        )
        return redirect('article_list')
    
    # برای درخواست GET
    users = User.objects.all()
    return render(request, 'article/create_article.html', {'users': users})