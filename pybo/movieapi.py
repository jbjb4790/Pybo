import os
from bs4 import BeautifulSoup as bs
import requests
import sys


def Mrank():
    url = 'https://movie.naver.com/movie/running/current.nhn'
    html = requests.get(url)
    if html.status_code != 200:
        sys.exit('데이터를 가져오지 못했습니다.')  # 응답이 없는 경우 프로그램 종료
    soup = bs(html.text, "html.parser")

    lst_soup = soup.find('ul', class_="lst_detail_t1").find_all('li')
    # print(lst_soup)
    moviedata = []
    for movie in lst_soup:
        mdata = {}
        title = movie.find('dt', class_='tit').find('a').text
        mdata['title'] = title
        image = movie.find('div', class_='thumb').find('img')['src']
        mdata['image'] = image
        star = movie.find('dd', class_='star').find('span', class_='num').text
        mdata['star'] = star
        genre = movie.find('span', class_='link_txt').find('a').text
        mdata['genre'] = genre
        moviedata.append(mdata)

    return moviedata






