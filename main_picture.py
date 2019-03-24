import requests
from bs4 import BeautifulSoup
import urllib.request
from time import sleep
import csv
import os


# step 1: 유기동물공고페이지에 접속해서 각 공고들의 상세 페이지 주소를 스크래이핑한다.
list = []
url_list = []
def step1_get_url_list():
    # 상세 페이지 주소를 담을 리스트
    for pp in range(1, 5):
        site = 'http://animal.go.kr/portal_rnl/abandonment/public_list.jsp?s_date=&e_date=&s_upr_cd=&s_org_cd=&s_up_kind_cd=&s_kind_cd=&s_name=&s_shelter_cd=&s_wrk_cd=&s_state=&s_state_hidden=&pagecnt=' + str(
            pp)
        response = requests.get(site)
        soup = BeautifulSoup(response.content, 'html.parser')
        div_list = soup.select('.thumbnail01 .thumbnail_btn01_2 a')
        for a in div_list:
            href = a.get('href')
            href = 'http://animal.go.kr' + href
            # 리스트에 담는다.
            url_list.append(href)
    return url_list

def step2_detail_html(url):
        global i

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        info_list = soup.select('.gonggoView td')
        if info_list[2].text.strip()[1] == "개":
            img_tag = soup.select(".boardBG img")
            print(img_tag)
            img_src = img_tag[0].get("src")
            img_name = img_tag[0].get("alt")
            img_url = 'http://animal.go.kr' + img_src
            urllib.request.urlretrieve(img_url, str(i) + str('.jpg'))
            print("img src:", img_src)
            print("img url:", img_url)
            print("img name:", img_name[5:21])

        else:
            pass


# step2~step3까지 반복
url_list = step1_get_url_list()
i = 0
for url in url_list:
    i = i + 1
    sleep(1)
    data_list = step2_detail_html(url)
    print('저장완료')
print('작업완료')
