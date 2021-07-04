from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import numpy as np

year = 1942
page_num = 1
url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
webpage_contents = requests.get(url).text
response = requests.get(url)
soup = BeautifulSoup(webpage_contents, "lxml")

dates, title, headlines = [], [], []

while True:
    print(url)
    if year == 2013:
        # print(len(dates), len(title), len(headlines))
        data = {'Date': dates, 'Title': title, 'Headline': headlines}
        world_history_df = pd.DataFrame(data)
        # print(world_history_df.head())
        world_history_df.to_csv('world_history_project.csv')
        sys.exit()
    webpage_contents = requests.get(url).text
    soup = BeautifulSoup(webpage_contents, "lxml")
    page_num += 1
    url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
    result = soup.find('div', {'class': 'col-xs-12 pagination-container'}).find('ul').find('li', {'class': 'next disabled'})

    # dates = []
    for li_tag in soup.find_all('li', {'class': 'media event'}):
        time_info = li_tag.find('time')
        # dates.append(time_info.attrs['datetime'])
        dates.append(time_info.text.strip())

    # title = []
    for h3_tag in soup.find_all('h3', {'class': 'media-heading'}):
        title_info = h3_tag.find('a')
        title.append((title_info.text.strip()))

    # headlines = []
    for div_tag in soup.find_all('div', {'class': 'media-body'}):
        try:
            p_tag = div_tag.find('p')
            headlines.append(p_tag.text.strip())
        except AttributeError:
            headlines.append('NO HEADLINE DATA ENTERED')

    if result is not None:
        year += 1
        page_num = 1
        url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)

    else:
        continue


