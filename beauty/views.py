from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from random import randint
from .models import Youtuber, Video, Cosmetic #, Viuser
import datetime

def pagnation(request, contexts, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT):
    paginator=Paginator(contexts, PAGE_ROW_COUNT)
    pageNum=request.GET.get('pageNum') # 현제 페이지
    
    totalPageCount=paginator.num_pages # 전체 페이지 갯수 
    
    try:
        contexts = paginator.page(pageNum)
    except PageNotAnInteger:
        contexts = paginator.page(1)
        pageNum = 1
    except EmptyPage:
        contexts = paginator.page(paginator.num_pages)
        pageNum = paginator.num_pages
        
    pageNum = int(pageNum)
    
    startPageNum = 1 + PAGE_DISPLAY_COUNT * int((pageNum - 1)/PAGE_DISPLAY_COUNT)
    endPageNum = startPageNum + PAGE_DISPLAY_COUNT-1

    if totalPageCount < endPageNum:
        endPageNum = totalPageCount
        
    bottomPages = range(startPageNum, endPageNum+1)

    return {
        'contexts': contexts,
        'pageNum': pageNum,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum,
    }


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

def video_list(request, period):
    if period == "all":
        videos = Video.objects.all().order_by('-hits')
    elif period == "month":
        today = datetime.datetime.now()
        month = today.month
        videos = Video.objects.filter(upload_at__month=month).order_by('-hits')
    elif period == "week":
        today = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        videos = Video.objects.filter(upload_at__gte=(today-seven_days)).order_by('-hits')
    else:
        redirect("beauty:combine_cosmetic")

    PAGE_ROW_COUNT = 10
    PAGE_DISPLAY_COUNT = 10

    contexts = pagnation(request, videos, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT)
    contexts['videos'] = contexts['contexts']
    del contexts['contexts']
    contexts['period'] = period
    
    return render(request, 'beauty/video_list.html', contexts)


cosmetic_kind = ['lip', 'brush']

def cosmetic_list(request, kind):
    if kind == 'all':
        cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    elif kind in cosmetic_kind:
        cosmetics = Cosmetic.objects.filter(category=kind).annotate(count=Count('video')).order_by('-count')
    else:
        redirect("beauty:combine_cosmetic")

    PAGE_ROW_COUNT = 10
    PAGE_DISPLAY_COUNT = 10

    contexts = pagnation(request, cosmetics, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT)
    contexts['cosmetics'] = contexts['contexts']
    del contexts['contexts']
    contexts['kind'] = kind

    return render(request, 'beauty/cosmetic_list.html', contexts)

def combine_cosmetic(request):
    cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    lips = Cosmetic.objects.filter(category='lip').annotate(count=Count('video')).order_by('-count')
    brushes = Cosmetic.objects.filter(category='brush').annotate(count=Count('video')).order_by('-count')

    return render(request, 'beauty/combine_cosmetic.html', {
        'cosmetics' : cosmetics,
        'lips' : lips,
        'brushes' : brushes,
    })


def combine_result(request):
    if request.method == 'POST':
        cosmetics = []
        video_cnt = {}
        for num in request.POST:
            try:
                cosmetic = get_object_or_404(Cosmetic, pk=num)
                cosmetics.append(cosmetic)

                for video in cosmetic.video_set.all():
                    try:
                        video_cnt[video.id] = video_cnt[video.id] + 1
                    except:
                        video_cnt[video.id] = 1
            except:
                pass
        
        videos = []
        for video_id, cnt in sorted(video_cnt.items(), key=lambda t : t[1], reverse=True)[0:10]:
            video = get_object_or_404(Video, pk=video_id)
            videos.append(video)

        return render(request, "beauty/combine_result.html", {
            'cosmetics' : cosmetics,
            'videos' : videos,
        })
    else:
        return redirect("beauty:combine_cosmetic")
