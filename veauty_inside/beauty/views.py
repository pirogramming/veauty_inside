from django.shortcuts import render, get_object_or_404, redirect
from .models import Youtuber, Video, Cosmetic #, Viuser

# Create your views here.
def home(request):
    youtubers = Youtuber.objects.all()
    videos = Video.objects.all()
    cosmetics = Cosmetic.objects.all()

    return render(request, 'beauty/home.html', {
        'youtubers' : youtubers,
        'videos' : videos,
        'cosmetics' : cosmetics,
    })