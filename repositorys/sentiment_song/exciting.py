import requests
import pandas as pd
from bs4 import BeautifulSoup
 
if __name__ == "__main__":
    RANK = 45
 
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    req = requests.get('https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=482778619', headers = header)
    html = req.text

    parse = BeautifulSoup(html, 'html.parser')

    titles = parse.find_all("div", {"class": "ellipsis rank01"})
    singers = parse.find_all("div", {"class": "ellipsis rank02"}) 

    title = []
    singer = []

    for t in titles:
        title.append(t.find('a').text)
    for s in singers:
        singer.append(s.find('span', {"class": "checkEllipsis"}).text)

    dataframe = pd.DataFrame({"title":title,"singer":singer})
    dataframe['exciting'] = 'exciting'
    dataframe = dataframe[['exciting','title','singer']]
    dataframe.to_csv(r'D:\S.saws.project\repository\sentiment_song\song_list\song_exciting.csv', index = False)