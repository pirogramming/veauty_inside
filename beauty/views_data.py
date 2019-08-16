from django.shortcuts import render, get_object_or_404, redirect
from random import randint
from .models import Youtuber, Video, Cosmetic, Bigcate, Smallcate
import datetime
import copy
import csv
import codecs
import os

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
    try:
        os.remove('output.csv')
    except:
        pass
    try:
        os.remove('encoded_output.csv')
    except:
        pass

    with open('output.csv', 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)

        cosmetics = []
        s_cate_cnt = 15
        for i in range(0, 50):
            s_cate = randint(1, s_cate_cnt)
            cosmetics.append({"s_cate"+str(s_cate):"cos"+str(i)})
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
            cos_set = []
            for _ in range(1, cos_cnt+1):
                cos_id = randint(0, 49)
                if not cos_id in id_set:
                    id_set.append(cos_id)
                    cos_set.append(cosmetics[cos_id])
            print(i, cos_set)

            wr.writerow([
                i,
                "title"+str(i),
                "www.youtube.com/"+str(i),
                "youtuber"+str(randint(1, 10)),
                randint(1, 1000000),
                upload
            ]+cos_set)        

    infile = codecs.open('output.csv', 'r', encoding='utf-8')
    outfile = codecs.open('encoded_output.csv', 'w', encoding='euc_kr')
    
    for line in infile:
        line = line.replace(u'\xa0', ' ')    # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
        outfile.write(line)
    
    infile.close()
    outfile.close()

    return render(request, "beauty/base.html")

def cosmetic_edit(request):
    if request.method =="POST":
        try:
            os.remove('real_output.csv')
        except:
            pass

        with open("encoded_output.csv") as f_in, open("real_output.csv", 'w', encoding='utf-8', newline='') as f_out:
            reader = csv.reader(f_in, delimiter=",")
            wr = csv.writer(f_out)

            for i, row in enumerate(reader):
                temp_cos = []
                j = 0
                while True:
                    try:
                        temp_cos.append(request.POST[str(i)+","+str(j)])
                        j = j + 1
                    except:
                        break
                wr.writerow(row[:6]+temp_cos)

    contexts = {}
    row_cos = []
    try:
        with open("real_output.csv", 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for i, row in enumerate(reader):
                row_cos.append(row[6:])
                contexts['range'] = range(0, i+1)
            contexts.update({
                    "row_cos" : row_cos
                })
    except:
        with open("encoded_output.csv", 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for i, row in enumerate(reader):
                row_cos.append(row[6:])
                contexts['range'] = range(0, i+1)
            contexts.update({
                    "row_cos" : row_cos
                })
    return render(request, "beauty/cosmetic_edit.html", contexts)

def processing_csv(request):
    Bigcate.objects.all().delete()
    Youtuber.objects.all().delete()
    Video.objects.all().delete()
    Cosmetic.objects.all().delete()
    Smallcate.objects.all().delete()

    for i in range(1, 5+1):
        bigcate = Bigcate()
        bigcate.name = 'b_cate'+str(i)
        bigcate.eng_name = 'eng_b_cate'+str(i)
        bigcate.save()

    small_cates = {}
    for i in range(1, 15+1):
        small_cates.update({
            's_cate'+str(i) : 'b_cate'+str(randint(1, 5))
        })

    with open("real_output.csv", 'r') as f:
        reader = csv.reader(f, delimiter=",")

        for row in reader:
            for youtuber_name in row[3:4]:
                try:
                    get_object_or_404(Youtuber, name=youtuber_name)
                except:
                    youtuber = Youtuber()
                    youtuber.name = youtuber_name
                    youtuber.save()

            for cos in row[6:]:
                temp_cos = list(cos.split(":"))
                print(temp_cos[-1].strip().replace("{", "").replace("}", "").replace("'", ""))

                small_cate = temp_cos[0].strip().replace("{", "").replace("}", "").replace("'", "")
                try:
                    get_object_or_404(Smallcate, name=small_cate)
                except:
                    smallcate = Smallcate()
                    smallcate.name = small_cate
                    smallcate.eng_name = 'eng_'+small_cate
                    smallcate.bigcate = get_object_or_404(Bigcate, name=small_cates[small_cate])
                    smallcate.save()

                cosmetic_name = temp_cos[-1].strip().replace("{", "").replace("}", "").replace("'", "")
                try:
                    get_object_or_404(Cosmetic, name=cosmetic_name)
                except:
                    cosmetic = Cosmetic()
                    cosmetic.name = cosmetic_name
                    cosmetic.category = get_object_or_404(Smallcate, name=small_cate)
                    cosmetic.save()

            video = Video()
            video.title = row[1]
            video.yt_url = row[2]
            video.youtuber = get_object_or_404(Youtuber, name=row[3])
            video.hits = row[4]
            video.upload_at = row[5][:10]
            video.save()
            for cos in row[6:]: 
                temp_cos = list(cos.split(":"))
                cos_name = temp_cos[-1].strip().replace("{", "").replace("}", "").replace("'", "")
                video.cosmetic.add(get_object_or_404(Cosmetic, name=cos_name))
    return render(request, "beauty/base.html")
    