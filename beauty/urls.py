from django.urls import path
from . import views

app_name = 'beauty'

urlpatterns = [
    path('', views.home, name="home"),
    path('video/<str:period>', views.video_list, name="video_list"),
    path('cosmetic/<str:kind>', views.cosmetic_list, name="cosmetic_list"),
    path('combinate/result', views.combine_result, name="combine_result"),
    path('combinate/<str:kind>', views.combine_cosmetic, name="combine_cosmetic"),
]