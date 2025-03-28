from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('unregistered-users/', unregistered_users_view, name='unregistered_users'),
    path('approve-user/<int:user_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', reject_user, name='reject_user'),
    path('registered-users/', registered_users_view, name='registered_users'),
    # Apis
    path('api_register/', UserNotRegisterCreateAPIView.as_view(), name='user_not_register_api'),
]
