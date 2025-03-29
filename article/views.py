from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from users.models import User  # مستقیماً مدل User سفارشی را وارد می‌کنیم

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
        if not title or not content or not author_id:
            users = User.objects.all()
            error_message = "لطفاً تمامی فیلدها را پر کنید."
            return render(request, 'article/create_article.html', {
                'users': users,
                'error_message': error_message,
                'title': title,
                'content': content
            })
        
        try:
            author = User.objects.get(id=author_id)
            article = Article.objects.create(
                title=title,
                content=content,
                author=author
            )
            return redirect('article_list')
        except User.DoesNotExist:
            users = User.objects.all()
            error_message = "کاربر انتخاب شده وجود ندارد."
            return render(request, 'article/create_article.html', {
                'users': users,
                'error_message': error_message,
                'title': title,
                'content': content
            })
    
    # برای درخواست GET
    users = User.objects.all()
    return render(request, 'article/create_article.html', {'users': users})