from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:kind>', views.profile, name='profile'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    # path('nickname_change/', views.MyNicknameChangeView.as_view(), name='nick_change'),
    path('video_scrap_processing', views.video_scrap_processing, name='video_scrap_processing'),
    path('cosmetic_scrap_processing', views.cosmetic_scrap_processing, name='cosmetic_scrap_processing'),
]
