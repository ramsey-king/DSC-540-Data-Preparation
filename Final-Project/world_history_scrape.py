from bs4 import BeautifulSoup
import requests
import sys

year = 2012
page_num = 1
url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
webpage_contents = requests.get(url).text
response = requests.get(url)
soup = BeautifulSoup(webpage_contents, "lxml")

headings = []

while True:
    print(url)
    if year == 2013:
        print(dates, headlines)
        sys.exit()
    webpage_contents = requests.get(url).text
    soup = BeautifulSoup(webpage_contents, "lxml")
    page_num += 1
    url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
    result = soup.find('div', {'class': 'col-xs-12 pagination-container'}).find('ul').find('li', {'class': 'next disabled'})

    dates = []
    for li_tag in soup.find_all('li', {'class': 'media-event'}):
        time_info = li_tag.find('time')
        print(time_info)
        dates.append(time_info.text.strip())

    headlines = []
    for div_tag in soup.find_all('div', {'class': 'media-body'}):
        p_tag = div_tag.find('p')
        headlines.append(p_tag.text.strip())

    if result is not None:
        year += 1
        page_num = 1
        url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)

    else:
        continue


