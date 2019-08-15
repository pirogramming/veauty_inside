from django.urls import path
from . import views

app_name = 'beauty'

urlpatterns = [
    path('', views.home, name="home"),
    path('video/', views.video_list, name="video_list"),
    path('video/<str:period>', views.video_list, name="video_list"),
    path('video_scrap/', views.video_scrap, name="video_scrap"),

    path('cosmetic/', views.cosmetic_list, name="cosmetic_list"),
    path('cosmetic/<str:kind>', views.cosmetic_list, name="cosmetic_list"),
    path('cosmetic_scrap/', views.cosmetic_scrap, name="cosmetic_scrap"),

    path('combine/result/', views.combine_result, name="combine_result"),
    path('combine_processing/', views.combine_processing, name="combine_processing"),

    path('combine/', views.combine_cosmetic, name="combine_cosmetic"),
    path('combine/<str:kind>', views.combine_cosmetic, name="combine_cosmetic"),
    
    path('cosmetic_pick/', views.cosmetic_pick, name="cosmetic_pick"),
    path('cosmetic_delete/', views.cosmetic_delete, name="cosmetic_delete"),
    path('cosmetic_reset/', views.cosmetic_reset, name="cosmetic_reset"),

    path('cosmetic_save/', views.cosmetic_save, name="cosmetic_save"),
    path('recommend_scrap/', views.recommend_scrap, name="recommend_scrap"),
]