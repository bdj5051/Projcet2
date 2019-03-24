import requests
from bs4 import BeautifulSoup
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

# step 2: step1에서 추출한 상세 페이지 주소를 돌면서 상세 페이지 HTML 데이터를 추출한다.
def step2_detail_html(url):

    # 상세 페이지의 html 데이터를 받아온다.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 공고 정보를 추출한다.
    info_list = soup.select('.gonggoView td')

    if info_list[2].text.strip()[1] == "개":
        global i
        no = info_list[1].text.strip()
        breed = info_list[2].text.strip()
        color = info_list[3].text.strip()
        sex = info_list[4].text.strip()
        neutralization = info_list[5].text.strip()
        birth_weight = info_list[6].text.strip()
        receipt_date = info_list[7].text.strip()
        place = info_list[8].text.strip()
        feature = info_list[9].text.strip()
        limit = info_list[10].text.strip()
        center_name = info_list[12].text.strip()
        center_tel = info_list[13].text.strip()
        center_add = info_list[14].text.strip()
        data_list = [i, no, breed, color, sex, neutralization, birth_weight, receipt_date, place, feature, limit,
                     center_name, center_tel, center_add]
        print(data_list)
        if os.path.exists('animal.csv') == False:
            # 헤더를 저장한다.
            with open('animal.csv', 'w', newline='', encoding='utf-8-sig') as fp:
                writer = csv.writer(fp)
                writer.writerow(
                    ['i', 'no', 'breed', 'color', 'sex', 'neutralization', 'birth_weight', 'receipt_date', 'place',
                     'feature', 'limit', 'center_name', 'center_tel', 'center_add'])
            # 데이터 저장

        with open('animal.csv', 'a', newline='', encoding='utf-8-sig') as fp2:
            writer2 = csv.writer(fp2)
            writer2.writerow(data_list)

    else:
        pass


def step3_save_csv(data):
    # 파일이 없다면 최초 저장
    if os.path.exists('animal.csv')==False:
        #헤더를 저장한다.
        with open('animal.csv', 'w', newline='', encoding='utf-8-sig') as fp:
            writer = csv.writer(fp)
            writer.writerow(['i', 'no', 'breed', 'color', 'sex', 'neutralization', 'birth_weight', 'receipt_date', 'place', 'feature', 'limit', 'center_name', 'center_tel', 'center_add'])
    # 데이터 저장

    with open('animal.csv', 'a', newline='', encoding='utf-8-sig') as fp2:
        writer2 = csv.writer(fp2)
        writer2.writerow(data)

    # step2~step3까지 반복
url_list = step1_get_url_list()
i = 0
for url in url_list:
    sleep(1)
    i = i + 1
    data_list = step2_detail_html(url)
    #step3_save_csv(data_list)
    print('저장완료')
print('작업완료')
