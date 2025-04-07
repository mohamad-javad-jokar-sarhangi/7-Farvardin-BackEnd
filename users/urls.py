from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('unregistered-users/', unregistered_users_view, name='unregistered_users'),
    path('approve-user/<int:user_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', reject_user, name='reject_user'),
    path('registered-users/', registered_users_view, name='registered_users'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('search-user/', search_user_view, name='search_user'),
    # Apis
    path('api_register/', UserNotRegisterCreateAPIView.as_view(), name='user_not_register_api'),
    path('api/is_user_pass/<str:phone_number>/', UserSearchAPIView.as_view(), name='is_user_pass_search_by_phone_api'),
]
