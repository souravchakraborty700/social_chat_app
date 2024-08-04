from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('app/', views.index, name='react_app'),
    path('api/users/', views.api_user_list, name='api_user_list'),
    path('api/received-interests/', views.api_received_interests, name='api_received_interests'),
    path('api/accept-interest/<int:interest_id>/', views.api_accept_interest, name='api_accept_interest'),
    path('api/reject-interest/<int:interest_id>/', views.api_reject_interest, name='api_reject_interest'),
    path('api/connect/', views.api_connect, name='api_connect'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('send_interest/<int:user_id>/', views.send_interest, name='send_interest'),
    path('received_interests/', views.received_interests, name='received_interests'),
    path('accept_interest/<int:interest_id>/', views.accept_interest, name='accept_interest'),
    path('reject_interest/<int:interest_id>/', views.reject_interest, name='reject_interest'),
    path('chat_box/<int:interest_id>/', views.chat_box, name='chat_box'),
    path('send_message/<int:interest_id>/', views.send_message, name='send_message'),
    path('connect/', views.connect, name='connect'),
    path('api/user/', views.api_user, name='api_user'),
    path('api/check-auth/', views.check_auth, name='check_auth'),
]