import bs4
import requests
import re

HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415;'
              ' _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2;'
              ' __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}

URL = "https://habr.com"

KEYWORDS = ['3D', 'Digital', 'Nixys', 'API', 'сервис']


def main():
    response = requests.get(URL, headers=HEADERS)
    text = response.text

    soup = bs4.BeautifulSoup(text, features="html.parser")

    articles = soup.find_all("article")
    for article in articles:
        previews = article.find_all(
            class_="article-formatted-body article-formatted-body article-formatted-body_version-2") \
                   + article.find_all(class_="article-formatted-body article-formatted-body "
                                             "article-formatted-body_version-1")
        previews = set(preview.text.strip() for preview in previews)

        for preview in previews:
            preview = re.sub(r'[.,!?/:;"]', ' ', preview)
            preview = preview.split()
            if set(preview) & set(KEYWORDS):
                date = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                href = article.find(class_="tm-article-snippet__title-link").attrs['href']
                title = article.find("h2").find("span").text
                result = f"{date} - {title} - {URL}{href}"
                print(result)


if __name__ == '__main__':
    main()
