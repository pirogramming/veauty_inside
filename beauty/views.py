from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Youtuber, Video, Cosmetic, Bigcate, Smallcate
from urllib import parse
from . import message_string as msg
import datetime

COSMETIC_SELECTION = {
    'all' : 'all',
    'interest' : 'interest',
    'my' : 'my',
}

def redirect_with_query(url_path, querystring, url_parameter=""):
    if url_parameter:
        response = redirect(url_path, url_parameter)
    else:
        response = redirect(url_path)
        
    response['Location'] += querystring
    
    return response

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
    return render(request, 'beauty/home.html')

def video_list(request, period=""):
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    seven_days = datetime.timedelta(days=7)

    VIDEO_FILTER = {
        "all" : Video.objects.all().order_by('-hits'),
        "month" : Video.objects.filter(upload_at__month=month).filter(upload_at__year=year).order_by('-hits'),
        "week" : Video.objects.filter(upload_at__gte=(today-seven_days)).order_by('-hits'),
    }

    if period == "":
        period = list(VIDEO_FILTER.keys())[0]

    videos = VIDEO_FILTER.get(period, None)

    if videos is None:
        return redirect("beauty:home")

    contexts = pagination(request, videos, 'videos')
    contexts.update({
        'period' : period,
        'big_categories' : Bigcate.objects.all(),
    })

    return render(request, 'beauty/video_list.html', contexts)

def video_scrap(request):
    if request.method == 'POST':
        videos = Video.objects.filter(pk__in=request.POST.getlist("video_id"))

        if videos:
            request.user.video.add(*videos)
            messages.success(request, msg.VIDEO_SCRAP)
        else:
            messages.warning(request, msg.NO_VIDEO_SELECT)

    if request.GET.get('q'):
        return redirect_with_query("beauty:search", '?q='+parse.quote(request.GET['q']))
    else:
        return redirect_with_query("beauty:video_list", '?pageNum='+request.POST['pageNum'], request.POST['period'])

def list_for_cosmetic(request, kind, combinate=False, PAGE_ROW_COUNT=10):
    contexts = {}

    try:
        smallcate = Smallcate.objects.get(eng_name=kind)

        #COSMETIC_FILTER insert necessary cosmetic instances
        cosmetics = Cosmetic.objects.filter(category=smallcate).annotate(count=Count('video')).order_by('-count')

        #contexts update
        contexts.update({
            'curr_small' : smallcate,
            'curr_big' : smallcate.bigcate,
            'small_categories' : smallcate.bigcate.smallcate_set.all(),
        })
    except Smallcate.DoesNotExist:
        #'cosmetic/' is same with 'cosmetic/all'
        if kind == "":
            kind = COSMETIC_SELECTION['all']

        COSMETIC_FILTER = {
            COSMETIC_SELECTION['all'] : Cosmetic.objects.annotate(count=Count('video')).order_by('-count'),
        }
        
        #COSMETIC_FILTER update at coemetic combaine page and user login state
        if combinate and request.user.is_authenticated:
            COSMETIC_FILTER.update({
                COSMETIC_SELECTION['interest'] : request.user.cosmetic.all().annotate(count=Count('video')).order_by('-count'),
                COSMETIC_SELECTION['my'] : request.user.my_cosmetic.all().annotate(count=Count('video')).order_by('-count'),
            })
    
        cosmetics = COSMETIC_FILTER.get(kind, None)

    if cosmetics is None:
        return 0
    else:
        contexts.update(pagination(request, cosmetics, 'cosmetics', PAGE_ROW_COUNT))
        contexts.update({
            'kind' : kind,
            'big_categories' : Bigcate.objects.all(),
        })

        return contexts

def cosmetic_list(request, kind=""):
    contexts = list_for_cosmetic(request, kind, combinate=False, PAGE_ROW_COUNT=10)
    if contexts == 0:
        return redirect("beauty:home")
    else:
        youtube_num = 5
        contexts.update({
            'yt_num' : youtube_num,
            'yt_range' : range(youtube_num),
        })
        return render(request, 'beauty/cosmetic_list.html', contexts)

def cosmetic_scrap(request):
    if request.method == 'POST':
        cosmetics = Cosmetic.objects.filter(pk__in=request.POST.getlist("cosmetic_id"))

        if request.POST['selection'] == COSMETIC_SELECTION['interest']:
            if cosmetics:
                request.user.cosmetic.add(*cosmetics)
                messages.success(request, msg.INTEREST_COS_SCRAP)
            else:
                messages.warning(request, msg.NO_INTEREST_SELECT)

        elif request.POST['selection'] == COSMETIC_SELECTION['my']:
            if cosmetics:
                request.user.my_cosmetic.add(*cosmetics)
                messages.success(request, msg.MY_COS_SCRAP)
            else:
                messages.warning(request, msg.NO_MY_SELECT)

    if request.GET.get('q'):
        return redirect_with_query("beauty:search", '?q='+parse.quote(request.GET['q']))
    else:
        return redirect_with_query("beauty:cosmetic_list", '?pageNum='+request.POST['pageNum'], request.POST['kind'])

def combine_cosmetic(request, kind=""):
    contexts = list_for_cosmetic(request, kind, combinate=True, PAGE_ROW_COUNT=15)
    storage = get_messages(request)
    for message in storage:
        contexts.update({
            'message_tags' : message.tags.split(" ")[1]
        })

    if contexts == 0:
        return redirect("beauty:home")
    else:
        contexts.update({
            'selected' : [get_object_or_404(Cosmetic, pk=pk) for pk in request.GET.getlist('c')],
            'query_cos' : (lambda x: '?c=' + '&c='.join(x) if x else "")(request.GET.getlist('c')),
        })
        return render(request, 'beauty/combine_cosmetic.html', contexts)

def cosmetic_pick(request):
    if request.method == "POST":
        querystring = request.POST['curr_query']
        cosmetics_id_list = request.POST.getlist('cosmetic_id')
        if cosmetics_id_list:
            query_list = querystring.split('&')

            for cos_id in cosmetics_id_list:
                cos_id_query = "c=" + cos_id

                if not cos_id_query in query_list:
                    querystring = querystring + "&c=" + cos_id

            messages.success(request, msg.PUT_IN_BASKET, extra_tags='pick')
        else:
            messages.warning(request, msg.NO_BASKET_SELECT, extra_tags='pick')
            
        return redirect_with_query("beauty:combine_cosmetic", '?' + querystring, request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", COSMETIC_SELECTION['all'])

def cosmetic_delete(request):
    if request.method == "POST":
        querystring = request.POST['curr_query']

        delete_query_list = ["c="+del_cos for del_cos in request.POST.getlist('del_cos')]
        if delete_query_list:
            query_list = querystring.split('&')
            query_list = [query_item for query_item in query_list if query_item not in delete_query_list]
            
            querystring = "&".join(query_list)

            messages.success(request, msg.DELETE_COS_IN_BASKET, extra_tags='basket')
        else:
            messages.warning(request, msg.NO_DELETE_COS, extra_tags='basket')
        
        return redirect_with_query("beauty:combine_cosmetic", '?' + querystring, request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", COSMETIC_SELECTION['all'])

def cosmetic_reset(request):
    if request.method == "POST":
        query_list = request.POST['curr_query'].split('&')
        cosmetic_have = False
        temp_list = []

        for query_item in query_list:
            if query_item[:2] == "c=":
                cosmetic_have = True
            else:
                temp_list.append(query_item)
        querystring = "&".join(temp_list)

        if cosmetic_have:
            messages.success(request, msg.RESET_BASKET, extra_tags='basket')
        else:
            messages.warning(request, msg.NO_BASKET, extra_tags='basket')

        return redirect_with_query("beauty:combine_cosmetic", '?' + querystring, request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", COSMETIC_SELECTION['all'])

def combine_processing(request):
    if request.method == 'POST':
        querystring = request.POST['curr_query']

        cosmetic_have = False
        for query_item in querystring.split('&'):
            if query_item[:2] == "c=":
                cosmetic_have = True
                break

        if cosmetic_have:
            return redirect_with_query("beauty:combine_result", '?' + querystring)
        else:
            messages.warning(request, msg.NO_BASKET, extra_tags='basket')
            return redirect_with_query("beauty:combine_cosmetic", '?' + querystring, request.POST['kind'])
    else:
        return redirect("beauty:combine_cosmetic", COSMETIC_SELECTION['all'])

def create_recomend(selected=[]):
    video_infos = {}
    for cosmetic in selected:
        for video in cosmetic.video_set.all():
            try:
                video_infos[video.id][1] = video_infos[video.id][1] + 1
            except KeyError:
                video_info = [video.hits, 1]
                video_infos[video.id] = video_info

    videos = []
    recomend_videos = sorted(video_infos.items(), key=lambda t : (t[1][1], t[1][0]), reverse=True)[0:20]

    for recomend_video in recomend_videos:
        video = get_object_or_404(Video, pk=recomend_video[0])
        videos.append(video)
    return videos

def combine_result(request):
    selected = [get_object_or_404(Cosmetic, pk=pk) for pk in request.GET.getlist('c')]
    videos = create_recomend(selected=selected)

    contexts = {
        'cosmetics' : selected,
        'videos' : videos,
    }

    storage = get_messages(request)
    for message in storage:
        contexts.update({
            'message_tags' : message.tags.split(" ")[1]
        })

    return render(request, "beauty/combine_result.html", contexts)

def cosmetic_save(request):
    querystring = request.POST['curr_query']

    if request.method == "POST":
        if request.user.is_authenticated:
            cosmetics = [get_object_or_404(Cosmetic, pk=query_item[2:]) for query_item in querystring.split('&') if query_item[:2] == "c="]

            if request.POST['selection'] == COSMETIC_SELECTION['interest']:
                request.user.cosmetic.add(*cosmetics)
                messages.success(request, msg.INTEREST_COS_SCRAP, extra_tags='cosmetic')
            elif request.POST['selection'] == COSMETIC_SELECTION['my']:
                request.user.my_cosmetic.add(*cosmetics)
                messages.success(request, msg.MY_COS_SCRAP, extra_tags='cosmetic')
        else:
            messages.info(request, msg.LOGIN_REQUIRE, extra_tags='cosmetic')

    return redirect_with_query("beauty:combine_result", '?' + querystring)

def recommend_scrap(request):
    querystring = request.POST['curr_query']

    if request.method == "POST":
        if request.user.is_authenticated:
            video_list = request.POST.getlist('video_id')

            if video_list:
                videos = Video.objects.filter(pk__in=video_list)
                request.user.video.add(*videos)
            
                messages.success(request, msg.VIDEO_SCRAP, extra_tags='video')
            else:
                messages.warning(request, msg.NO_VIDEO_SELECT, extra_tags='video')
        else:
            messages.info(request, msg.LOGIN_REQUIRE, extra_tags='video')

    return redirect_with_query("beauty:combine_result", '?' + querystring)

def search(request):
    q = request.GET['q']
    videos = Video.objects.filter(title__contains=q)
    cosmetics = Cosmetic.objects.filter(name__contains=q)

    return render(request, "beauty/search_result.html", {
        'videos' : videos,
        'cosmetics' : cosmetics,
        'q' : q,
        'big_categories' : Bigcate.objects.all(),
    })
        
