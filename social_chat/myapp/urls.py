from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('send_interest/<int:user_id>/', views.send_interest, name='send_interest'),
    path('received_interests/', views.received_interests, name='received_interests'),
    path('accept_interest/<int:interest_id>/', views.accept_interest, name='accept_interest'),
    path('reject_interest/<int:interest_id>/', views.reject_interest, name='reject_interest'),
    path('chat_box/<int:interest_id>/', views.chat_box, name='chat_box'),
    path('send_message/<int:interest_id>/', views.send_message, name='send_message'),
    path('connect/', views.connect, name='connect'),
]
