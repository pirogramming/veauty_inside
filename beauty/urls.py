from django.urls import path
from . import views, views_data

app_name = 'beauty'

urlpatterns = [
    path('create_test_DB', views_data.create_test_DB, name="create_test_DB"),
    path('create_test_csv', views_data.create_test_csv, name="creat_test_csv"),
    path('convert_xlsx_to_csv', views_data.convert_xlsx_to_csv, name="convert_xlsx_to_csv"),
    path('create_category_csv', views_data.create_category_csv, name="create_category_csv"),
    path('cosmetic_edit/<int:num>', views_data.cosmetic_edit, name="cosmetic_edit"),
    path('processing_csv', views_data.processing_csv, name="processing_csv"),

    path('', views.home, name="home"),
    path('video/', views.video_list, name="video_list"),
    path('video/<str:period>', views.video_list, name="video_list"),
    path('video_scrap', views.video_scrap, name="video_scrap"),

    path('cosmetic/', views.cosmetic_list, name="cosmetic_list"),
    path('cosmetic/<str:kind>', views.cosmetic_list, name="cosmetic_list"),
    path('cosmetic_scrap', views.cosmetic_scrap, name="cosmetic_scrap"),

    path('combine/result', views.combine_result, name="combine_result"),
    path('combine_processing', views.combine_processing, name="combine_processing"),

    path('combine/', views.combine_cosmetic, name="combine_cosmetic"),
    path('combine/<str:kind>', views.combine_cosmetic, name="combine_cosmetic"),
    
    path('cosmetic_pick', views.cosmetic_pick, name="cosmetic_pick"),
    path('cosmetic_delete', views.cosmetic_delete, name="cosmetic_delete"),
    path('cosmetic_reset', views.cosmetic_reset, name="cosmetic_reset"),

    path('cosmetic_save', views.cosmetic_save, name="cosmetic_save"),
    path('recommend_scrap', views.recommend_scrap, name="recommend_scrap"),
]