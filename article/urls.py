from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.article_list, name='article_list'),
    path('create/', views.create_article, name='create_article'),
    path('detail/<int:pk>/', views.article_detail, name='article_detail'),
]
