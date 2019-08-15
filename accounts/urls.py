from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:kind>', views.profile, name='profile'),
    path('profile/combine/result/', views.combine_result, name='combine_result'),
    path('video_scrap_processing', views.video_scrap_processing, name='video_scrap_processing'),
    path('cosmetic_scrap_processing', views.cosmetic_scrap_processing, name='cosmetic_scrap_processing'),
]
