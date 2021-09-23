
# 입력한 아이디를 통해 개인 게시물 탭으로 가는 url을 리턴하는 함수

def insta_searching(word):
    url = "https://www.instagram.com/" + word
    return url


from bs4 import BeautifulSoup
from  selenium import webdriver
import time
import pandas as pd
import re
from selenium.common.exceptions import NoSuchElementException

# webdriver를 간편하게 사용하기위한 코드

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# 인스타그램 로그인화면을 킴

driver.get("https://www.instagram.com/accounts/login/")

# 브라우저가 완전히 로딩되는것을 기다리기 위한 명령어

time.sleep(1) 
#콘솔에 아이디 입력
email = input("아이디입력: ")
# 로그인 화면의 아이디 입력 칸을 class이름을 통해 찾음(' ' 안의 내용이 클래스)   
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
# 해당 칸의 내용을 지움
input_id.clear()
# 콘솔에 입력받은 아이디를 아이디 입력 칸에 보냄
input_id.send_keys(email)
#콘솔에 비밀번호 입력
password = input("비밀번호입력: ")
# 로그인 화면의 비밀번호 입력 칸을 class이름을 통해 찾음(' ' 안의 내용이 클래스)   
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
# 해당 칸의 내용을 지움
input_pw.clear()
# 콘솔에 입력받은 비밀번호를 비밀번호 입력 칸에 보냄
input_pw.send_keys(password)
# 로그인 버튼 클릭
input_pw.submit()
time.sleep(3)
# word에 아이디 값이 들어감
word = email
# 개인 게시물 탭의 url을 얻음
url = insta_searching(word)
# 해당 url로 이동
driver.get(url)

time.sleep(2)

#게시일자와 내용을 저장하기 위한 배열 생성

insta_dict = {'date': [],'text': []}

#첫번쨰 게시물의 위치를 class값을 이용해 찾음

first_post = driver.find_element_by_class_name('eLAPa')
#첫번쨰 게시물 클릭
first_post.click()
num = 0
seq = 0
#정보를 가져오는 속도를 측정하기위한 코드
start = time.time()

# 크롤링할 게시물의 개수를 정함

while num < 11  :
    #다음 게시물로 넘어가는 버튼이 있을떄까지 실행
    try:
        # 다음 게시물로 넘어가는 버튼을 찾았다면
        if driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow'):
            #0,20,40개마다 크롤링해오는 시간을 출력
            if seq % 20 == 0:
                print('{}번째 수집 중'.format(seq), time.time() - start, sep = '\t')
 
 
            #class값을 이용해 해당 게시물의 게시일이 저장되어있는 칸을 찾음
            time_raw = driver.find_element_by_css_selector('time.FH9sR.Nzb55')
            #해당 게시물의 게시 일자와 게시 시간까지 가져오는 코드(게시한 시간까지는 사이트에 저장되지않아 게시 일자만 표시됨)
            time_info = pd.to_datetime(time_raw.get_attribute('datetime')).normalize()
            #insta_dict의 date 열에 크롤링한 게시 일자를 저장함
            insta_dict['date'].append(time_info)
 
            #class값을 이용해 해당 게시물의 내용이 저장되어있는 칸을 찾아 해당 내용을 문자열로 나눔(hello world python을 hello, world, python 으로 바꿈)
            raw_info = driver.find_element_by_css_selector('div.C4VMK').text.split()
            #게시글의 내용만을 가져오기 위한 배열 생성
            text = []
            #문자열로 나누어진 게시물의 길이만큼 반복문 실행
            for i in range(len(raw_info)):
                # 첫번째 text는 아이디므로 제외
                if i == 0:
                    pass 
                else:
                    # 나누어진 문자열 중에 #이 포함되었다면 제외
                    if '#' in raw_info[i]:
                        pass
                    # 그 외의 문자열은 text에 저장함
                    else:
                        text.append(raw_info[i])
            # 쓸데없는 띄어쓰기를 제거
            clean_text = ' '.join(text)
            #ihnsta_dict의 text열에 크롤링한 게시글 내용을 저장
            insta_dict['text'].append(clean_text)

            seq += 1
            #크롤링할 수 있는 최대 게시글의 숫자를 100개로 저장함
            if seq == 100:
                break
            #다음 게시글로 넘어감        
            driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
            time.sleep(1.5)
            
        #다음 게시글로 넘어가는 버튼을 못찾았으면 조건문 종료
        else:
            break
    # 다음 게시물로 넘어가는 버튼이 없을때의 예외 처리
    except NoSuchElementException:
        driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
        time.sleep(2)
    num += 1

#데이터프레임 만들고 엑셀로 저장하기
results_df = pd.DataFrame(insta_dict)
results_df.to_csv(r'D:\S.saws.project\repository\insta_crawler\insta_crawler.csv',index=False) 