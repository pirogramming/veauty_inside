#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import csv
import time
import json


wait_between_requests = 3
# url 내 정보를 크롤링하는데에 약 3초간의 딜레이가 필요

channel_name = 'Hines382'
# 크롤링하고 싶은 youtube 채널 작성

youtube_base = 'https://www.youtube.com/'
# url을 생성할 때 주소의 앞부분에 붙여주기 위한 주소
 
parent_folder = ''  # users or channel or empty
# 설명 필요#####

def get_soup(url):
	# '{youtube_base}/user/{channel_name}/playlists' url인자를 받아
	# url에게 html 데이터를 요청하고 bs4 객체를 return하는 함수

    result = requests.get(url)
    # url 주소로 GET 요청(request)를 보냈고 
    # 서버에서는 그 요청을 받아 뭔가를 처리한 후 요청자인 나에게 응답(response)
    # result 값은 성공하면 <Response [200]>을 저장

    if result.status_code != 200: return None
    # 성공하여 200값을 return하는지 확인
    time.sleep(wait_between_requests)
    # 데이터를 크롤링하기 위해 딜레이
    return BeautifulSoup(result.text, 'html.parser')
	# html.parser모듈을 통하여 url에 대한 html데이터 크롤링

def channel_section_links(channel_name):
    """return 값:
       list of 
       { 'title': <section title>, 
         'link': <url to section play lists> 
       }"""

    global parent_folder
    # 설명 필요######

    soup = get_soup(f'{youtube_base}/user/{channel_name}/playlists')
    # getsoup 함수에 '{youtube_base}/user/{channel_name}/playlists'를 url인자로 전달
    # getsoup 함수로 부터 url의 html 데이터를 soup에 저장, 없으면 none값이 저장됨
    # i.e. https://www.youtube.com//user/gjenkinslbcc/playlists

    if soup is None or 'This channel does not exist.' in soup.text:
    	# soup의 html 데이터안에 tag부분만 제외한 soup.text 부분에
    	# 'This channel does not exist.' 문자열 존재 확인
        url = f'{youtube_base}/channel/{channel_name}/playlists'
        soup = get_soup(url)
        # '{youtube_base}/channel/{channel_name}/playlists'을 url로 받아 다시 한번 get_soup 함수 실행
        if soup is None or 'This channel does not exist.' in soup.text:
            raise ValueError(
                'The channel does not exists: ' + channel_name)
            # 존재하지 않을 시 최종적으로 channel 없음 error 띄움
        parent_folder = 'channel/'
        # 설명 필요####

    play_list_atags = \
        soup.find_all('a',
                      {'href': re.compile(f'{channel_name}/playlists')})
    # 정규표현식을 사용하여 '{channel_name}/playlists'가 href로 포함된 a 태그를 play_list_atags 리스트에 요소로 저장
    elements = [{'title': x.text.strip(),
                 'link': fix_url(x['href'])} for x in play_list_atags
                if x.span and
                ('shelf_id=0' not in x['href'])]
    # play_list_atags 내 요소를 하나씩 x에 저장 후 if 문 동작
    # 요소 내 span에 둘러싸인 값이 존재 && 요소의 href 태그 내 shelf_id=0이 없을 시 동작
    # 동작하면 title에 요소의 값을 저장
    # link에 요소의 href값을 fix_url의 인자로 보내어 return 값을 저장

    if len(elements) == 0:
        url = f'{youtube_base}{parent_folder}{channel_name}/playlists'
        elements = [ {'title': 'no sections', 'link': url}]
        # 재생목록이 없는 경우 url을 {youtube_base}{parent_folder}{channel_name}/playlists'로 저장
        # elements를 [ {'title': 'no sections', 'link': url}]로 저장
        # i.e.  https://www.youtube.com/channel/UCHFklTiPnl2TrCgLLtdfENw/playlists
    return elements
    # return깂은 재생목록을 보여주는 페이지의 큰 재생목록의 title과 url


def fix_url(url):
    if url[0] == '/':
        return youtube_base + url
        # i.e. '/user/gjenkinslbcc/playlists?view=1&sort=dd&shelf_id=0'링크로 받아오는 것을
        # 앞에 youtube.com을 붙여 접근 가능한 full 주소로 고쳐줌(상대 경로를 절대 경로로 바꿔줌)
    else:
        return url
        # 아닐 시 그대로 return


def get_playlists(section):
    """returns list of list of
    { 'title': <playlist tile>, <link to all playlist videos> }"""
    global parent_folder
    # 초기값은 빈 값
    print(f"  getting playlists for section: {section['title']}")
    # section의 인자로 받은 title 출력
    soup = get_soup(section['link'])
    # section의 인자로 받은 link를 get_soup 함수 실행
    # i.e. https://www.youtube.com//user/gjenkinslbcc/playlists?view=50&sort=dd&shelf_id=2
    if soup is None: # no playlist, create dummy with default link
        url = f'{youtube_base}{parent_folder}{channel_name}/videos'
        return [
           {'title': 'No Playlists', 'link':url }]
    # soup값이 없을 시 [{'title': 'No Playlists', 'link':url }] return
    atags = soup('a', class_='yt-uix-tile-link')
    # a태그의 class가 'yt-uix-tile-link'인 값 파싱

    playlists = []
    for a in atags:
        title = a.text
        # atags를 통해 모든 플레이리스트의 title값 파싱
        if title != 'Liked videos': # liked videos 제외
            url = fix_url(a['href'])
            # atags를 통해 모든 플레이리스트 url값 파싱
            playlists.append({'title': title, 'link': url})
            #playlists에 모든 값 저장

    if not playlists:  # 플레이리스트 없을 시
        url = f'{youtube_base}/{parent_folder}{channel_name}/videos'
        return [{'title': 'No Playlists', 'link': url}]

    return playlists

def parse_video(vurl):
    # return dict of
    # title, link, views, publication_date,
    # description, short_link, likes, dislikes

    d = {'link': vurl, 'views': None, 'short_link': vurl,
         'likes': None, 'dislikes': None}

    # now get video page and pull information from it
    vsoup = get_soup(vurl)
    # 동영상 링크에 대해 크롤링

    o = vsoup.find('title')
    # vsoup 내 title 파싱 후 o에 저장
    vtitle = o.text.strip()
    # o값 내 양옆 공란 제거
    xending = ' - YouTube'
    d['title'] = vtitle[:-len(xending)] \
        if vtitle.endswith(xending) else vtitle
    print(f"      processing video '{d['title']}'" )
    # title을 긁어올 때 뒤에 ' - YouTube'가 딸려오기 때문에 단어 제거

    # o is used in the code following to
    # catch missing data targets for scrapping
    o = vsoup.find('div', class_='watch-view-count')
    if o:
        views = o.text
        d['views'] = ''.join(c for c in views if c in '0123456789')
    # 조회수 크롤링

    o = vsoup.find('strong', class_='watch-time-text')
    d['publication_date'] = \
        o.text[len('게시일 :') - 1:] if o else ''
    # 게시일 크롤링

    o = vsoup.find('div', id='watch-description-text')
    d['description'] = o.text if o else ''
    # description 크롤링

    o = vsoup.find('meta', itemprop='videoId')
    if o:
        vid = o['content']
        d['short_link'] = f'https://youtu.be/{vid}'
    # video id 크롤링

    o = vsoup.find('button',
                   class_='like-button-renderer-like-button')
    if o:
        o = o.find('span', class_='yt-uix-button-content')
        d['likes'] = o.text if o else ''
    # 좋아요 수 크롤링

    o = vsoup.find('button',
                   class_='like-button-renderer-dislike-button')
    if o:
        o = o.find('span', class_='yt-uix-button-content')
        d['dislikes'] = o.text if o else ''
    # 싫어요 수 크롤링

    return d


def add_videos(playlist):
    """find videos in playlist[link]
    and add their info as playlist[videos] as list"""
    surl = playlist['link']
    # 작은 playlist의 url을 surl에 저장
    soup = get_soup(surl)
    # 작은 플레이리스트의 html 파싱하여 soup에 저장
    print(f"    getting videos for playlist: {playlist['title']}")

    videos = []

    # items are list of video a links from list
    items = soup('a', class_='yt-uix-tile-link')
    # a 태그의 class가 'yt-uix-tile-link'인 태그 items에 저장
    # items는 작은 플레이리스트의 동영상 목록들임

    # note first part of look get info from playlist page item,
    # and the the last part opens the video and gets more details
    if len(items) > 0:
        for i in items:
        # 각각의 items i에 하나씩 저장
            d = dict()
            vurl = fix_url(i['href'])
            # 동영상 url을 vurl에 저장
            t = i.find_next('span', {'aria-label': True})
            # 동영상의 span 태그 중 aria=label값이 존재하는 것 t에 저장
            # t는 동영상의 재생 시간임
            d['time'] = t.text if t else 'NA'
            # d 딕셔너리에 t저장

            d.update(parse_video(vurl))
            videos.append(d)
            # videos에 d를 append

    else:  # must be only one video
        d = {'time': 'NA'}
        d.update(parse_video(surl))
        videos.append(d)

    # add new key to this playlist of list of video infos
    playlist['videos'] = videos
    print()


def tag(t,c):
    return f'<{t}>{c}</{t}>' # return html tag with content


def link(text, url): # return a tag with content and link
    return f'<a href="{url}">{text}</a>'

def html_out(channel, sections):
    """create and write channel_name.html file"""
    title = f'YouTube Channel {channel}'
    f = open(f'{channel}.html','w')
    template = ('<!doctype html>\n<html lang="en">\n<head>\n'
                '<meta charset="utf-8">'
                '<title>{}</title>\n</head>\n'
                '<body>\n{}\n</body>\n</html>')

    parts = list()
    parts.append(tag('h1', title))

    for s in sections:
        parts.append(tag('h2',link(s['title'], s['link'])))
        for pl in s['playlists']:
            parts.append(tag('h3', link(pl['title'], pl['link'])))
            if len(pl) == 0:
                parts.append('<p>Empty Playlist</p>')
            else:
                parts.append('<ol>')
                for v in pl['videos']:
                    t = '' if v['time'] == 'NA' else f" ({v['time']})"
                    parts.append(tag('li', link(v['title'],
                                     v['short_link']) + t))
                parts.append('</ol>')
    f.write(template.format(channel, '\n'.join(parts)))
    f.close()


def csv_out(channel, sections):
    """ create and output channel_name.csv
    file for import into a spreadsheet or DB"""
    headers = ('channel,section,playlist,video,'
               'link,time,views,publication date,'
               'likes,dislikes,description').split(',')

    with open(f'{channel}.csv', 'w') as csv_file:
        csvf = csv.writer(csv_file, delimiter=',')
        csvf.writerow(headers)
        for section in sections:
            for playlist in section['playlists']:
                for video in playlist['videos']:
                    v = video
                    line = [channel,
                            section['title'],
                            playlist['title'],
                            v['title']]
                    line.extend([v['short_link'],
                                 v['time'], v['views'],
                                 v['publication_date'],
                                 v['likes'], v['dislikes'],
                                 v['description']])
                    csvf.writerow(line)


def process_channel(channel_name):
    sections = channel_section_links(channel_name)
    # sections에 channel_section_links의 return 값인 elements를 저장
    # 큰 재생목록 저장
    # i.e. [{'title': 'Python Data Structures and Algorithms Class - CS22', 'link': 'https://www.youtube.com//user/gjenkinslbcc/playlists?view=50&sort=dd&shelf_id=2'}]
    for section in sections:
        section['playlists'] = get_playlists(section)
        # sections의 값들을 section에 하나씩 넣어 get_playlists 함수로 돌려 작은 재생목록의 url과 title 저장
        # 작은 재생목록 저장
		# i.e. {'title': 'Python Data Structures and Algorithms Class - CS22', 'link': 'https://www.youtube.com//user/gjenkinslbcc/playlists?view=50&sort=dd&shelf_id=2', 'playlists': [{'title': '1: CS22 - Python Data Structures/Algorithms Class - Introduction', 'link': 'https://www.youtube.com//playlist?list=PLtbC5OfOR8aqA6CJwWTRUITgGpUy1Umr3'}, {'title': '2: CS22 - Analysis', 'link': 'https://www.youtube.com//playlist?list=PLtbC5OfOR8aops-jzO_fzNJ-6Q6_Tblro'}]
		# 큰 플레이리스트를 저장한 dict에 작은 플레이리스트들의 title과 link를 저장
        for playlist in section['playlists']:
        	# 작은 플레이리스트들을 playlist에 하나씩 저장
            add_videos(playlist)
            # 동영상에 대한 데이터 딕셔너리 videos 데이터 return
    return sections
    # 큰 재생목록에 해당하는 작은 재상목록의 동영상들의 dict 값 return


if __name__ == '__main__':
    # find channel name by going to channel
    # and picking last element from channel url
    # for example my channel url is:
    #   https://www.youtube.com/user/gjenkinslbcc
    # my channel name is gjenkinslbcc in this url
    # this is set near top of this file
    # if the channel is of the form:
    # https://www.youtube.com/channel/xyz then supply xyz

    print(f'finding sections for youtube.com {channel_name}')
    sections = process_channel(channel_name)

    # save sections structure to json file
    with open(f'{channel_name}.json','w') as f:
        f.write(json.dumps(sections, sort_keys=True, indent=4))

    html_out(channel_name, sections)  # create web page of channel links

    # create a csv file of video info for import into spreadsheet
    csv_out(channel_name, sections)


    print(f"Program Complete,\n  '{channel_name}.html' and"
          f" '{channel_name}.csv' have been" 
          f" written to current directory")