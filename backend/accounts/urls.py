from django.urls import path
from .views import LoginAPIView, LogoutAPIView, CheckAuthStatusAPIView, UserDetailsAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('check_auth_status/', CheckAuthStatusAPIView.as_view(), name='check_auth_status'),
    path('user/details/<str:username>/', UserDetailsAPIView.as_view(), name='user-details'),
]