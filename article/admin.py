from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author_name')
    list_filter = ('created_at', 'updated_at')

admin.site.register(Article, ArticleAdmin)