#-*- coding:utf-8 -*-
import re
import pandas as pd 

'''
def filtering(self):
	filter = re.compile('[^ ㄱ-ㅣ가-힣]+')
	#url_list_proto 내 모든 url 중 유튜버의 콘텐츠만 갖고 오기 위한 정규식을 filter에 저장
	#filter의 조건에 맞게 url_list_proto 내 모든 url 필터링하여 result에 저장
	results = filter.sub('', self)
	result.append(results)
'''

def input_csv():
	df = pd.read_csv('pony.csv', sep=',', encoding='EUC-KR') 
	column_df = df['description'] 
	return column_df

def one_description(self):
	for i in range(self.size-1):
		des_lists.append(self.values[i])
	return des_lists

def making_list(self):
	global b
	for i in range(len(self)):
		str(self[i]).replace("'","")
		str(self[i]).replace('"',"")
		filter1=str(self[i]).split('-')
		filter2=str(self[i]).split('?')
		filter3=str(self[i]).split('ㅡ')

		while '' in filter1:
			filter1.remove('')

		while '' in filter2:
			filter2.remove('')

		while '' in filter3:
			filter3.remove('')

		if len(filter1)>=len(filter2):
			a=filter1
		else:
			a=filter2
		if len(filter3)>len(a):
			a=filter3
		del a[len(a)-1]
		b.append(a)
	return b

def strip(self):
	for i in range(len(b)):
		for y in range(len(b[i])):
			b[i][y]=b[i][y].strip() 
	return b

def category_filtering


if __name__ == '__main__':

	filter1=[]
	filter2=[]
	filter3=[]
	result=[]
	des_lists=[]
	a=[]
	b=[]
	category_list=['스킨/토너/토닉', '로션/에멀젼', '미스트', '쿠션', '파운데이션', '컨실러', '파우더', '블러쉬(블러셔, 브론징)', '컨투어링(하이라이터)', '프라이머', 'UV프로텍터', '아이브로우', '아이라이너', '마스카라', '섀도우(글리터)', '립/립스틱/틴트', '립케어/립밤/립글로스/립 오일']
	h={}

	description=input_csv()
	des_list=one_description(description)
	one_des=making_list(des_list)
	c=strip(one_des)

'''
	for i in range(len(category_list)):
		for y in range(len(a)):
			if category_list[i] in a[y]:
				h[category_list[i]] = a[y]

	for key in h.keys():
		print(key)
		print(h[key])
'''
'''
	for i in range(len(a)):
		print("{}번째 item: {}".format(i+1, a[i]))
'''


		#print(key, ":", h[key])
