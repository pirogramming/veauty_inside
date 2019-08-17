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

def create_category_csv(request):
    if request.method =="POST":
        try:
            os.remove('category.csv')
        except:
            pass

        with open("temp_category.csv", 'w', encoding='utf-8', newline='') as f_out:
            wr = csv.writer(f_out)

            i = 0
            while True:
                temp_cate = []
                try:
                    if request.POST[str(i)+","+str(0)] != "" and request.POST[str(i)+","+str(1)] != "":
                        temp_cate.append(request.POST[str(i)+","+str(0)])
                        temp_cate.append(request.POST[str(i)+","+str(1)])

                        wr.writerow(temp_cate)
                except:
                    break
                i = i + 1
            try:
                if request.POST['add']:
                    wr.writerow(["-", "-"])
            except:
                pass
        
        infile = codecs.open('temp_category.csv', 'r', encoding='utf-8')
        outfile = codecs.open('category.csv', 'w', encoding='euc_kr')
        
        for line in infile:
            line = line.replace(u'\xa0', ' ')    # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
            outfile.write(line)

        infile.close()
        outfile.close()

        os.remove('temp_category.csv')

    try:
        with open("category.csv", "r") as f:
            pass
    except:
        with open("temp_category.csv", "w", encoding='utf-8', newline='') as f:
            wr = csv.writer(f)

            for i in range(1, 5+1):
                for j in range(i*4-3, i*4+1):
                    wr.writerow(["b_cate"+str(i), "eng_b_cate"+str(i),"s_cate"+str(j),"eng_s_cate"+str(i)])

        infile = codecs.open('temp_category.csv', 'r', encoding='utf-8')
        outfile = codecs.open('category.csv', 'w', encoding='euc_kr')
        
        for line in infile:
            line = line.replace(u'\xa0', ' ')    # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
            outfile.write(line)

        infile.close()
        outfile.close()

        os.remove('temp_category.csv')

    contexts = {}
    row_cate = []

    with open("category.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")

        for i, row in enumerate(reader):
            row_cate.append(row)
            contexts['range'] = range(0, i+1)

        contexts.update({
                "row_cate" : row_cate
            })

    Bigcate.objects.all().delete()
    Smallcate.objects.all().delete()
    with open("category.csv", 'r') as f:
        reader = csv.reader(f, delimiter=",")

        for row in reader:
            row_dict = {
                'bigcate' : row[0],
                'bigcate_eng' : row[1],
                'smallcate' : row[2],
                'smallcate_eng' : row[3],
            }
            try:
                Bigcate.objects.get(name=row_dict['bigcate'])
            except Bigcate.DoesNotExist:
                bigcate = Bigcate()
                bigcate.name = row_dict['bigcate']
                bigcate.eng_name = row_dict['bigcate_eng']
                bigcate.save()
                print(bigcate)

            smallcate = Smallcate()
            smallcate.name = row_dict['smallcate']
            smallcate.eng_name = row_dict['smallcate_eng']
            smallcate.bigcate = get_object_or_404(Bigcate, name=row_dict['bigcate'])
            smallcate.save()

    return render(request, "beauty/category_edit.html", contexts)

def create_test_csv(request):
    bigcates = Bigcate.objects.all()
    smallcates = Smallcate.objects.all()
    try:
        os.remove('output.csv')
    except:
        pass
    try:
        os.remove('original_output.csv')
    except:
        pass

    with open('original_output.csv', 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        
        cosmetics = []        
        for i in range(0, 50):
            s_cate = smallcates[randint(0, len(bigcates)-1)].name
            cosmetics.append({s_cate:"코스메틱"+str(i)})

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

    infile = codecs.open('original_output.csv', 'r', encoding='utf-8')
    outfile = codecs.open('output.csv', 'w', encoding='euc_kr')
    
    for line in infile:
        line = line.replace(u'\xa0', ' ')    # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
        outfile.write(line)

    infile.close()
    outfile.close()

    return render(request, "beauty/base.html")

def cosmetic_edit(request):
    if request.method =="POST":
        with open("output.csv") as f_in, open("temp_output.csv", 'w', encoding='utf-8', newline='') as f_out:
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
        os.remove('output.csv')
    
        infile = codecs.open('temp_output.csv', 'r', encoding='utf-8')
        outfile = codecs.open('output.csv', 'w', encoding='euc_kr')
        
        for line in infile:
            line = line.replace(u'\xa0', ' ')    # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
            outfile.write(line)

        infile.close()
        outfile.close()

        os.remove('temp_output.csv')

    contexts = {}
    row_cos = []

    with open("output.csv", 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(reader):
            row_cos.append(row[6:])
            contexts['range'] = range(0, i+1)
        contexts.update({
                "row_cos" : row_cos
            })

    return render(request, "beauty/cosmetic_edit.html", contexts)

def processing_csv(request):
    #Caution!! these codes will delete all DB
    Youtuber.objects.all().delete()
    Video.objects.all().delete()
    Cosmetic.objects.all().delete()
    #################################
    with open("output.csv", 'r') as f:
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
                cosmetic_name = temp_cos[-1].strip().replace("{", "").replace("}", "").replace("'", "")
                try:
                    Cosmetic.objects.get(name=cosmetic_name)
                except Cosmetic.DoesNotExist:
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
    