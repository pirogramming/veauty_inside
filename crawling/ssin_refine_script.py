#-*- coding:utf-8 -*-
import re
import pandas as pd 
import copy
import csv

'''
def filtering(self):
	filter = re.compile('[^ ㄱ-ㅣ가-힣]+')
	#url_list_proto 내 모든 url 중 유튜버의 콘텐츠만 갖고 오기 위한 정규식을 filter에 저장
	#filter의 조건에 맞게 url_list_proto 내 모든 url 필터링하여 result에 저장
	results = filter.sub('', self)
	result.append(results)
'''

def input_csv():
	df = pd.read_csv('ssin.csv', sep=',', encoding='CP949') 
	column_df = df['description'] 
	return column_df

def one_description(self):
	for i in range(self.size-1):
		des_lists.append(self.values[i])
	return des_lists

def making_list(self):
	global b
	for i in range(len(self)):
		self[i]=str(self[i]).replace("'","")
		self[i]=str(self[i]).replace('"',"")
		self[i]=str(self[i]).replace(':','')
		self[i]=str(self[i]).replace('#',"=")
		filter1=str(self[i]).split('[')
		filter2=str(self[i]).split('-')
		'''

		filter3=str(self[i]).split('ㅡ')
		#filter4=str(self[i]).split('#')
		
		'''

		while '' in filter1:
			filter1.remove('')
		while '' in filter2:
			filter2.remove('')
		'''
		while '' in filter3:
			filter3.remove('')

		#while '' in filter4:
		#	filter4.remove('')
		'''
		
		if len(filter1)>=len(filter2):
			a=filter1
		else:
			a=filter2
		'''
		if len(filter3)>len(a):
			a=filter3
		'''
		#if len(filter4)>len(a):
		#	a=filter4

		del a[len(a)-1]
		b.append(a)
	return b

def strip(self):
	for i in range(len(b)):
		for y in range(len(b[i])):
			b[i][y]=b[i][y].strip() 
	return b

def category_filtering(self):
	global dic
	for y in range(len(c)):
		for z in range(len(c[y])):
			for i in range(len(dic)):
				if list(dic.keys())[i] in c[y][z]:
					dic[list(dic.keys())[i]].append(c[y][z])
					break
				elif '/' in list(dic.keys())[i]:
					ww=list(dic.keys())[i].split('/')
					for p in range(len(ww)):
						if ww[p] in c[y][z]:
							dic[list(dic.keys())[i]].append(c[y][z])
							break
				else:
					if list(dic.keys())[i]=='zzz':
						dic['zzz'].append(c[y][z])
					pass
		c[y]=dic
		dic = {'립/립스틱/틴트':[], '립케어/립밤/립글로스/립 오일':[], '메이크업 베이스':[], '프라이머':[], '비비크림/씨씨크림/BB/CC/비비/씨씨':[], '파운데이션':[], '쿠션':[], '파우더/팩트':[], '컨실러/톤실러':[], '블러셔/블러쉬/치크':[], '하이라이터':[], '메이크업픽서':[], '셰이딩/쉐딩/컨투어/컨투어링/컨투어러/쉐이딩/쉐이드/셰이드/셰딩/섀딩/브론징':[], '톤업크림':[], '선케어':[], '아이라이너/라이너':[], '아이브로우/브로우':[], '마스카라':[], '아이섀도/섀도우/쉐도우':[], '에센스/앰플/세럼':[], '로션/에멀젼':[], '페이스 오일':[], '아이케어/아이크림':[], '미스트':[], '젤':[], '크림':[], '스킨/토너/토닉/워터':[], '브러쉬':[], '아이래쉬/속눈썹':[], 'zzz':[]}
	return c
		#print(dic)
	#for i in range(len(c)):
		#for y in range(len(c[i])):
		#print(c[i])
'''
def dd(y,z):
	global dic
	for i in range(len(dic)):
		if list(dic.keys())[i] in c[y][z]:
			dic[list(dic.keys())[i]].append(c[y][z])
			break
		else:
			if list(dic.keys())[i]=='zzz':
				dic['zzz'].append(c[y][z])
			pass
		return dic
'''

def csv_out(d):
	""" create and output channel_name.csv
	file for import into a spreadsheet or DB"""
	#headers = ('로션/에멀젼, 페이스 오일, 아이케어, 미스트, 젤, 메이크업 베이스, 프라이머, 비비크림/씨씨크림, 파운데이션, 쿠션, 파우더/팩트, 컨실러, 블러셔, 하이라이터, 메이크업픽서, 셰이딩, 톤업크림, 선케어, 아이라이너, 아이브로우, 립/립스틱/틴트, 립케어/립밤/립글로스/립 오일, 마스카라/픽서, 아이섀도, 에센스/앰플/세럼, 크림, 스킨/토너, zzz').split(',')
	global line
	with open('ssin_refine.csv', 'w', encoding='EUC-KR') as csv_file:
		csvf = csv.writer(csv_file, delimiter=',')
		#csvf.writerow(headers)
		for y in range(len(d)):
			for z in range(len(d[y])):
				'''
				line = [d[y]['스킨/토너/토닉'], d[y]['로션/에멀젼'], 
						d[y]['미스트'], d[y]['기타'], d[y]['쿠션'],
						d[y]['파운데이션'], d[y]['컨실러'],d[y]['파우더'], d[y]['블러쉬/블러셔/브론징'],
						d[y]['컨투어링/하이라이터'], d[y]['프라이머'], d[y]['UV프로텍터'],
						d[y]['아이브로우'],d[y]['아이라이너'], d[y]['마스카라'], d[y]['섀도우/글리터'],
						d[y]['립/립스틱/틴트'], d[y]['립케어/립밤/립글로스/립 오일'], d[y]['zzz']]
				'''

				line.append(d[y][z])
			csvf.writerow(line)
			line=[]

def refined(self):
	global t
	for y in range(len(d)):
		for z in range(len(d[y])):
			for p in range(len(list(d[y].values())[z])):
			#print(len((list(d[y].keys())[z].values())))
			#for p in range(len((list(d[y].keys)[z].values()))):
				q=str(list(d[y].keys())[z])+':'+str((list(d[y].values())[z])[p])
				t.append(q)
		d[y]=t
		t=[]
	return d

if __name__ == '__main__':

	filter1=[]
	filter2=[]
	filter3=[]
	result=[]
	des_lists=[]
	a=[]
	b=[]
	#category_list=['스킨/토너/토닉', '로션/에멀젼', '미스트', '쿠션', '파운데이션', '컨실러', '파우더', '블러쉬(블러셔, 브론징)', '컨투어링(하이라이터)', '프라이머', 'UV프로텍터', '아이브로우', '아이라이너', '마스카라', '섀도우(글리터)', '립/립스틱/틴트', '립케어/립밤/립글로스/립 오일']
	h={}
	e=[[]]
	g=[]
	dic = {'립/립스틱/틴트':[], '립케어/립밤/립글로스/립 오일':[], '메이크업 베이스':[], '프라이머':[], '비비크림/씨씨크림/BB/CC/비비/씨씨':[], '파운데이션':[], '쿠션':[], '파우더/팩트':[], '컨실러/톤실러':[], '블러셔/블러쉬/치크':[], '하이라이터':[], '메이크업픽서':[], '셰이딩/쉐딩/컨투어/컨투어링/컨투어러/쉐이딩/쉐이드/셰이드/셰딩/섀딩/브론징':[], '톤업크림':[], '선케어':[], '아이라이너/라이너':[], '아이브로우/브로우':[], '마스카라':[], '아이섀도/섀도우/쉐도우':[], '에센스/앰플/세럼':[], '로션/에멀젼':[], '페이스 오일':[], '아이케어/아이크림':[], '미스트':[], '젤':[], '크림':[], '스킨/토너/토닉/워터':[], '브러쉬':[], '아이래쉬/속눈썹':[], 'zzz':[]}
	line=[]
	li=[]
	t=[]

	description=input_csv()
	des_list=one_description(description)
	one_des=making_list(des_list)
	c=strip(one_des)
	#e=copy.deepcopy(c)
	d=category_filtering(c)
	refined(d)
	print(d)
	csv_out(d)

'''


	for key in h.keys():
		print(key)
		print(h[key])
'''
'''
	for i in range(len(a)):
		print("{}번째 item: {}".format(i+1, a[i]))
'''


		#print(key, ":", h[key])
