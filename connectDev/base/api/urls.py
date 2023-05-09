from django.urls import path
from . import views

urlpatterns = [
    path('rooms/',views.get_Rooms),
    path('rooms/<str:index>/',views.get_Room),
]
