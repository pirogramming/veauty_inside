from django.shortcuts import render, get_object_or_404, redirect
from random import randint
from .models import Youtuber, Video, Cosmetic, Bigcate, Smallcate
import datetime
import copy
import csv
import codecs

def create_test_DB(request):
    #test db 생성
    #Caution! These codes will delete all records!!!
    '''
    if request.user.is_superuser:
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
    return redirect("login")

def create_test_csv(request):
    with open('output.csv', 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)

        cosmetics = {}
        s_cate_cnt = randint(10, 20)
        for i in range(1, 50+1):
            s_cate = randint(1, s_cate_cnt)
            try:
                cosmetics[s_cate].append(i)
            except:
                cosmetics[s_cate] = [i]
        print(cosmetics)

        for i in range(1, 100+1):
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

            cos_cnt = randint(1, 15)
            id_set = []
            for _ in range(1, cos_cnt+1):
                cos_id = randint(1, 100)
                if not cos_id in id_set:
                    id_set.append(cos_id)

            wr.writerow([
                i,
                "title"+str(i),
                "www.youtube.com/"+str(i),
                "youtuber"+str(randint(1, 10)),
                randint(1, 1000000),
                upload
            ])
        

    infile = codecs.open('output.csv', 'r', encoding='utf-8')
    outfile = codecs.open('real_output.csv', 'w', encoding='euc_kr')
    
    for line in infile:
        line = line.replace(u'\xa0', ' ')    # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
        outfile.write(line)
    
    infile.close()
    outfile.close()

    return render(request, "beauty/base.html")
