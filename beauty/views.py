from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Youtuber, Video, Cosmetic, Bigcate, Smallcate
from urllib import parse
from . import message_string as msg
import datetime

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
        response = redirect("beauty:search")
        response['Location'] = response['Location']+'?q='+parse.quote(request.GET['q'])
    else:
        response = redirect("beauty:video_list", request.POST['period'])
        response['Location'] += '?pageNum='+request.POST['pageNum']

    return response

def list_for_cosmetic(request, kind, combinate=False, PAGE_ROW_COUNT=10):
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

    contexts.update(pagination(request, cosmetics, 'cosmetics', PAGE_ROW_COUNT))
    contexts.update({
        'kind' : kind,
        'big_categories' : Bigcate.objects.all(),
    })

    return contexts

def cosmetic_list(request, kind=""):
    contexts = list_for_cosmetic(request, kind)
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

        if request.POST['selection'] == 'interest':
            request.user.cosmetic.add(*cosmetics)
            if cosmetics:
                messages.success(request, msg.INTEREST_COS_SCRAP)
            else:
                messages.warning(request, msg.NO_INTEREST_SELECT)

        elif request.POST['selection'] == 'my':
            request.user.my_cosmetic.add(*cosmetics)
            if cosmetics:
                messages.success(request, msg.MY_COS_SCRAP)
            else:
                messages.warning(request, msg.NO_MY_SELECT)

    if request.GET.get('q'):
        response = redirect("beauty:search")
        response['Location'] = response['Location']+'?q='+parse.quote(request.GET['q'])
    else:
        response = redirect("beauty:cosmetic_list", request.POST['kind'])
        response['Location'] += '?pageNum=' + request.POST['pageNum']
   
    return response

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
            'curr_cos' : request.GET.getlist('c'),
            'query_cos' : (lambda x: '?c=' + '&c='.join(x) if x else "")(request.GET.getlist('c')),
        })
        return render(request, 'beauty/combine_cosmetic.html', contexts)

def cosmetic_pick(request):
    if request.method == "POST":
        querystring = (lambda x: '?c=' + '&c='.join(x) + "&" if x else "?")(request.POST.getlist('curr_cos'))

        cosmetics_list = request.POST.getlist('cosmetic_id')
        if cosmetics_list:
            messages.success(request, msg.PUT_IN_BASKET, extra_tags='pick')
        else:
            messages.warning(request, msg.NO_BASKET_SELECT, extra_tags='pick')

        for c in cosmetics_list:
            if not c in request.POST.getlist('curr_cos'):
                querystring = querystring + "c=" + c + "&"

        response = redirect("beauty:combine_cosmetic", request.POST['kind'])
        response['Location'] += (querystring + "pageNum=" + request.POST['pageNum'])
        return response
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def cosmetic_delete(request):
    if request.method == "POST":
        querystring = '?'

        delete_list = request.POST.getlist('del_cos')
        if delete_list:
            messages.success(request, msg.DELETE_COS_IN_BASKET, extra_tags='basket')
        else:
            messages.warning(request, msg.NO_DELETE_COS, extra_tags='basket')

        for c in request.POST.getlist('curr_cos'):
            if not c in delete_list:
                querystring = querystring + "c=" + c + "&"

        response = redirect("beauty:combine_cosmetic", request.POST['kind'])
        response['Location'] += (querystring + "pageNum=" + request.POST['pageNum'])
        return response
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def cosmetic_reset(request):
    if request.method == "POST":
        if request.POST['distinction'] == 'y':
            messages.success(request, msg.RESET_BASKET, extra_tags='basket')
        else:
            messages.warning(request, msg.NO_BASKET, extra_tags='basket')

        response = redirect("beauty:combine_cosmetic", request.POST['kind'])
        response['Location'] += "?pageNum=" + request.POST['pageNum']
        return response
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def combine_processing(request):
    if request.method == 'POST':
        current_list = request.POST.getlist('curr_cos')
        if current_list:
            querystring = (lambda x: '?c=' + '&c='.join(x) if x else "?")(current_list)

            response = redirect("beauty:combine_result")
            response['Location'] += querystring
            return response
        else:
            messages.warning(request, msg.NO_BASKET, extra_tags='basket')
            return redirect("beauty:combine_cosmetic", 'all')
    else:
        return redirect("beauty:combine_cosmetic", 'all')

def create_recomend(selected=[]):
    video_infos = {}
    for cosmetic in selected:
        for video in cosmetic.video_set.all():
            try:
                video_infos[video.id][1] = video_infos[video.id][1] + 1
            except:
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
    if request.method == "POST":
        if request.user.is_authenticated:
            cosmetics = Cosmetic.objects.filter(pk__in=request.POST.getlist('cosmetic_id'))
            if request.POST['selection'] == 'interest':
                request.user.cosmetic.add(*cosmetics)
                messages.success(request, msg.INTEREST_COS_SCRAP, extra_tags='cosmetic')
            elif request.POST['selection'] == 'my':
                request.user.my_cosmetic.add(*cosmetics)
                messages.success(request, msg.MY_COS_SCRAP, extra_tags='cosmetic')
        else:
            messages.info(request, msg.LOGIN_REQUIRE, extra_tags='cosmetic')


    querystring = (lambda x: '?c=' + '&c='.join(x) if x else "?")(request.POST.getlist('cosmetic_id'))
  
    response = redirect("beauty:combine_result")
    response['Location'] += querystring 
    return response

def recommend_scrap(request):
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


    querystring = (lambda x: '?c=' + '&c='.join(x) if x else "?")(request.POST.getlist('cosmetic_id'))

    response = redirect("beauty:combine_result")
    response['Location'] += querystring 
    return response

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
        
