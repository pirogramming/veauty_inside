from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from random import randint
from .models import Youtuber, Video, Cosmetic, Bigcate, Smallcate #, Viuser
import datetime

selected = []

def pagnation(request, contexts, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT, contexts_name):
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
        contexts_name: contexts,
        'pageNum': pageNum,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum,
    }


# Create your views here.
def home(request):
    #test db 생성
    '''
    for i in range(1, 5+1):
        bigcate = Bigcate()
        bigcate.name = 'bigcate'+str(i)
        bigcate.eng_name = 'eng_bigcate'+str(i)
        bigcate.save()
    bigcates = Bigcate.objects.all()
    
    for i in range(1, 20+1):
        smallcate = Smallcate()
        smallcate.bigcate = bigcates[randint(0, len(bigcates)-1)]
        smallcate.name = 'smallcate'+str(i)
        smallcate.eng_name = 'eng_smallcate'+str(i)
    smallcates = Smallcate.objects.all()

    for i in range(1, 100+1):
        cosmetic = Cosmetic()
        cosmetic.category = smallcates[randint(0, len(smallcates)-1)]
        cosmetic.name = 'cosmetic'+str(i)
        cosmetic.save()
    cosmetics = Cosmetic.objects.all()

    for i in range(1, 10+1):
        youtuber = Youtuber()
        youtuber.name = 'youtuber'+str(i)
        youtuber.save()
    youtubers = Youtuber.objects.all()
    
    #youtubers = Youtuber.objects.all()
    #cosmetics = Cosmetic.objects.all()
    
    for i in range(1, 150+1):
        video = Video()
        video.title = 'video'+str(i)
        video.yt_url = 'http://www.youtube.com'
        video.youtuber = youtubers[randint(0, len(youtubers)-1)]
        video.hits = randint(1, 1000000)
        
        dt = datetime.datetime.now()
        year = randint(dt.year-2, dt.year)
        if year < dt.year:
            month = randint(1, 12)
            day = randint(1, 28)
        else:
            month = randint(1, dt.month)
            if month < dt.month:
                day = randint(1, 28)
            else:
                day = randint(1, dt.day)
        upload = datetime.datetime.strptime(str(year)+'-'+str(month)+'-'+str(day), "%Y-%m-%d")
        video.upload_at = upload
        video.save()

        cos_cnt = randint(1, 15)
        id_set = []
        for j in range(1, cos_cnt+1):
            cos_id = randint(0, len(cosmetics)-1)
            cosmetic = cosmetics[cos_id]
            if not cos_id in id_set:
                id_set.append(cos_id)
                video.cosmetic.add(cosmetic)
    '''
    return render(request, 'beauty/home.html')

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
        return redirect("beauty:home")

    PAGE_ROW_COUNT = 10
    PAGE_DISPLAY_COUNT = 10

    contexts = pagnation(request, videos, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT, 'videos')
    contexts['period'] = period
    contexts['big_categories'] = Bigcate.objects.all()
    
    return render(request, 'beauty/video_list.html', contexts)

def cosmetic_list(request, kind):
    bigcates = Bigcate.objects.all()

    if kind == 'all':
        cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    else:
        smallcate_eng_name = [smallcategory.eng_name for smallcategory in Smallcate.objects.all()]
        if kind in smallcate_eng_name:
            curr_smallcate = get_object_or_404(Smallcate, eng_name=kind)
            curr_bigcate = get_object_or_404(Bigcate, pk=curr_smallcate.bigcate.pk)
            smallcates = curr_bigcate.smallcate_set.all()
            cosmetics = Cosmetic.objects.filter(category=curr_smallcate).annotate(count=Count('video')).order_by('-count')
        else:
            return redirect("beauty:home")

    PAGE_ROW_COUNT = 10
    PAGE_DISPLAY_COUNT = 10

    contexts = pagnation(request, cosmetics, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT, 'cosmetics')
    contexts['kind'] = kind
    contexts['big_categories'] = bigcates

    if kind != 'all':
        contexts['curr_big'] = curr_bigcate
        contexts['curr_small'] = curr_smallcate
        contexts['small_categories'] = smallcates

    return render(request, 'beauty/cosmetic_list.html', contexts)

# fix : global variable 'selected' User model의 필드로 교체
def combine_cosmetic(request, kind):
    bigcates = Bigcate.objects.all()

    if kind == 'all':
        cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    else:
        smallcate_eng_name = [smallcategory.eng_name for smallcategory in Smallcate.objects.all()]
        if kind in smallcate_eng_name:
            curr_smallcate = get_object_or_404(Smallcate, eng_name=kind)
            curr_bigcate = get_object_or_404(Bigcate, pk=curr_smallcate.bigcate.pk)
            smallcates = curr_bigcate.smallcate_set.all()
            cosmetics = Cosmetic.objects.filter(category=curr_smallcate).annotate(count=Count('video')).order_by('-count')
        else:
            return redirect("beauty:home")

    PAGE_ROW_COUNT = 10
    PAGE_DISPLAY_COUNT = 10

    contexts = pagnation(request, cosmetics, PAGE_ROW_COUNT, PAGE_DISPLAY_COUNT, 'cosmetics')
    contexts['kind'] = kind
    contexts['big_categories'] = bigcates

    if kind != 'all':
        contexts['curr_big'] = curr_bigcate
        contexts['curr_small'] = curr_smallcate
        contexts['small_categories'] = smallcates

    if request.method == "POST":
        try:
            request.POST['reset_selected']
            selected.clear()
            contexts['selected'] = selected

            return render(request, 'beauty/combine_cosmetic.html', contexts)
        except:
            pass

        try:
            request.POST['delete_selected']
            nums = []
            for num in request.POST:
                try:
                    nums.append(int(num)-1)
                except:
                    pass
            for num in sorted(nums, reverse=True):
                del selected[num]

            contexts['selected'] = selected

            return render(request, 'beauty/combine_cosmetic.html', contexts)
        except:
            pass

        for num in request.POST:
            try:
                selection = get_object_or_404(Cosmetic, pk=num)
                if not selection in selected:
                    selected.append(selection)
            except:
                pass
    
    contexts['selected'] = selected

    return render(request, 'beauty/combine_cosmetic.html', contexts)


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
        print(len(video_cnt))
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
