from django.urls import path
from . import views

app_name = 'beauty'

urlpatterns = [
    path('', views.home, name="home"),
]