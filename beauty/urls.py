from django.urls import path
from . import views

app_name = 'beauty'

urlpatterns = [
    path('', views.home, name="home"),
    path('video/', views.video_list, name="video_list"),
    path('cosmetic/', views.cosmetic_list, name="cosmetic_list"),
    path('combinate/', views.combine_cosmetic, name="combine_cosmetic"),
]