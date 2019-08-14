from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from random import randint
from .models import Youtuber, Video, Cosmetic, Bigcate, Smallcate
from accounts.models import User
import datetime

selected = []

def pagination(request, contexts, contexts_name, PAGE_ROW_COUNT=10, PAGE_DISPLAY_COUNT=10):
    paginator=Paginator(contexts, PAGE_ROW_COUNT)
    pageNum=request.GET.get('pageNum') # 현재 페이지
    
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
        'PAGE_ROW_COUNT' : PAGE_ROW_COUNT,
        'pageNum': pageNum,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum,
    }

def home(request):
    #test db 생성
    '''
    Bigcate.objects.all().delete()
    Youtuber.objects.all().delete()
    Video.objects.all().delete()
    Cosmetic.objects.all().delete()
    Smallcate.objects.all().delete()

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
        smallcate.save()
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

def video_list(request, period=""):
    if period == "all" or period == "":
        period = "all"
        videos = Video.objects.all().order_by('-hits')
    elif period == "month":
        today = datetime.datetime.now()
        year = today.year
        month = today.month
        videos = Video.objects.filter(upload_at__month=month).filter(upload_at__year=year).order_by('-hits')
    elif period == "week":
        today = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        videos = Video.objects.filter(upload_at__gte=(today-seven_days)).order_by('-hits')
    else:
        return redirect("beauty:home")

    contexts = pagination(request, videos, 'videos')
    contexts['period'] = period
    contexts['big_categories'] = Bigcate.objects.all()
    contexts['user_videos'] = (lambda x : request.user.video.all() if x else [])(request.user.is_authenticated)
    
    return render(request, 'beauty/video_list.html', contexts)

def video_scrap(request):
    if request.method == 'POST':
        for num in request.POST:
            try:
                video = get_object_or_404(Video, pk=num)
                request.user.video.add(video)
            except:
                pass
    response = redirect("beauty:video_list", request.POST['period'])
    response['Location'] += '?pageNum='+request.POST['pageNum']
    return response

def list_for_cosmetic(request, kind, combinate=False):
    addtional_cate = (lambda x : ['interest', 'my'] if x else [])(combinate)
    contexts = {}

    if kind == 'all' or kind == "":
        kind = "all"
        cosmetics = Cosmetic.objects.annotate(count=Count('video')).order_by('-count')
    elif kind in addtional_cate and request.user.is_authenticated:
        if kind == 'interest':
            cosmetics = request.user.cosmetic.all().annotate(count=Count('video')).order_by('-count')
        elif kind == 'my':
            cosmetics = request.user.my_cosmetic.all().annotate(count=Count('video')).order_by('-count')
    else:
        smallcate_eng_name = [smallcategory.eng_name for smallcategory in Smallcate.objects.all()]
        if kind in smallcate_eng_name:
            contexts['curr_small'] = get_object_or_404(Smallcate, eng_name=kind)
            contexts['curr_big'] = get_object_or_404(Bigcate, pk=contexts['curr_small'].bigcate.pk)
            contexts['small_categories'] = contexts['curr_big'].smallcate_set.all()
            cosmetics = Cosmetic.objects.filter(category=contexts['curr_small']).annotate(count=Count('video')).order_by('-count')
        else:
            return 0

    contexts.update(pagination(request, cosmetics, 'cosmetics'))
    contexts['kind'] = kind
    contexts['big_categories'] = Bigcate.objects.all()

    return contexts

def cosmetic_list(request, kind=""):
    contexts = list_for_cosmetic(request, kind)
    if contexts == 0:
        return redirect("beauty:home")
    else:
        youtube_num = 5
        contexts['yt_num'] = youtube_num
        contexts['yt_range'] = range(youtube_num)
        contexts['user_cosmetics'] = (lambda x : request.user.cosmetic.all() if x else [])(request.user.is_authenticated)
        
        return render(request, 'beauty/cosmetic_list.html', contexts)

def cosmetic_scrap(request):
    if request.method == 'POST':
        if request.POST['selection'] == 'Interest':
            for num in request.POST:
                try:
                    cosmetic = get_object_or_404(Cosmetic, pk=num)
                    request.user.cosmetic.add(cosmetic)
                except:
                    pass
        elif request.POST['selection'] == 'MY':
            for num in request.POST:
                try:
                    my_cosmetic = get_object_or_404(Cosmetic, pk=num)
                    request.user.my_cosmetic.add(my_cosmetic)
                except:
                    pass
        
    response = redirect("beauty:cosmetic_list", request.POST['kind'])
    response['Location'] += '?pageNum='+request.POST['pageNum']
    return response

def combine_cosmetic(request, kind=""):
    contexts = list_for_cosmetic(request, kind, combinate=True)
        
    if contexts == 0:
        return redirect("beauty:home")
    else:
        contexts['selected'] = selected
        return render(request, 'beauty/combine_cosmetic.html', contexts)

def cosmetic_pick(request):
    if request.method == "POST":
        for num in request.POST:
            try:
                selection = get_object_or_404(Cosmetic, pk=num)
                if not selection in selected:
                    selected.append(selection)
            except:
                pass
        return redirect("beauty:combine_cosmetic", request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def cosmetic_delete(request):
    if request.method == "POST":
        nums = []
        for num in request.POST:
            try:
                nums.append(int(num)-1)
            except:
                pass
        for num in sorted(nums, reverse=True):
            del selected[num]

        return redirect("beauty:combine_cosmetic", request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def cosmetic_reset(request):
    if request.method == "POST":
        selected.clear()
        return redirect("beauty:combine_cosmetic", request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def combine_processing(request):
    if request.method == 'POST':
        return redirect("beauty:combine_result")
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def combine_result(request):
    video_infos = {}
    for cosmetic in selected:
        for video in cosmetic.video_set.all():
            try:
                video_infos[video.id][1] = video_infos[video.id][1] + 1
            except:
                video_info = [video.hits, 1]
                video_infos[video.id] = video_info

    videos = []
    recomend_videos = sorted(video_infos.items(), key=lambda t : (t[1][1], t[1][0]), reverse=True)[0:10]

    for recomend_video in recomend_videos:
        video = get_object_or_404(Video, pk=recomend_video[0])
        videos.append(video)

    return render(request, "beauty/combine_result.html", {
        'cosmetics' : selected,
        'videos' : videos,
    })

def cosmetic_save(request):
    if request.method == "POST" and request.user.is_authenticated:
        if request.POST['selection'] == 'interest':
            for num in request.POST:
                try:
                    cosmetic = get_object_or_404(Cosmetic, pk=num)
                    request.user.cosmetic.add(cosmetic)
                except:
                    pass
        elif request.POST['selection'] == 'my':
            for num in request.POST:
                try:
                    my_cosmetic = get_object_or_404(Cosmetic, pk=num)
                    request.user.my_cosmetic.add(my_cosmetic)
                except:
                    pass
    
    return redirect("beauty:combine_result")

def recommend_scrap(request):
    if request.method == "POST" and request.user.is_authenticated:
        for num in request.POST:
            try:
                video = get_object_or_404(Video, pk=num)
                request.user.video.add(video)
            except:
                pass
    
    return redirect("beauty:combine_result")
        
