from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Youtuber, Video, Cosmetic #, Viuser
import datetime

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

def video_list(request):
    today = datetime.datetime.now()
    seven_days = datetime.timedelta(days=7)
    month = today.month
    videos_all = Video.objects.all().order_by('-hits')
    videos_month = Video.objects.filter(upload_at__month=month).order_by('-hits')
    videos_week = Video.objects.filter(upload_at__gte=(today-seven_days)).order_by('-hits')

    return render(request, 'beauty/video_list.html', {
        'videos_all' : videos_all,
        'videos_month' : videos_month,
        'videos_week' : videos_week,
    })

def cosmetic_list(request):
    cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    lips = Cosmetic.objects.filter(category='lip').annotate(count=Count('video')).order_by('-count')
    brushes = Cosmetic.objects.filter(category='brush').annotate(count=Count('video')).order_by('-count')

    return render(request, 'beauty/cosmetic_list.html', {
        'cosmetics' : cosmetics,
        'lips' : lips,
        'brushes' : brushes,
    })

def combine_cosmetic(request):
    if request.method == 'POST':
        cosmetics = []
        for num in request.POST:
            try:
                cosmetic = get_object_or_404(Cosmetic, pk=num)
                cosmetics.append(cosmetic)
            except:
                pass
        return render(request, 'beauty/combine_result.html', {
            'cosmetics' : cosmetics,
        })
    else:
        cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    lips = Cosmetic.objects.filter(category='lip').annotate(count=Count('video')).order_by('-count')
    brushes = Cosmetic.objects.filter(category='brush').annotate(count=Count('video')).order_by('-count')

    return render(request, 'beauty/combine_cosmetic.html', {
        'cosmetics' : cosmetics,
        'lips' : lips,
        'brushes' : brushes,
    })
