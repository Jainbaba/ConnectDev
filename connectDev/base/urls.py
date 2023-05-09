"""_summary_"""
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home_page,name='home'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_User,name='logout'),
    path('register/',views.register_page,name='register'),
    path('room/<str:index>/',views.room_page,name='room'),
    path('create-room/',views.create_room,name='create-room'),
    path('profile/<str:index>',views.profile_page,name='user-profile'),
    path('update-user/',views.update_user,name='update-user'),
    path('topics/',views.topics_page,name='topics'),
    path('activity/',views.activity_page,name='activity'),
    path('update-room/<str:index>/',views.update_room,name='update-room'),
    path('delete-room/<str:index>/',views.delete_room,name='delete-room'),
    path('delete-message/<str:index>/',views.delete_message,name='delete-message'),
]

 