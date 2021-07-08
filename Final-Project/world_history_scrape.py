from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import numpy as np

year = 2012 # CHANGE BACK TO 1942 WHEN READY TO TURN IN
page_num = 1
url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
webpage_contents = requests.get(url).text
response = requests.get(url)
soup = BeautifulSoup(webpage_contents, "lxml")

dates, title, headlines = [], [], []


def get_dates():
    for li_tag in soup.find_all('li', {'class': 'media event'}):
        time_info = li_tag.find('time')
        # dates.append(time_info.attrs['datetime'])
        dates.append(time_info.text.strip())


def get_titles():
    for h3_tag in soup.find_all('h3', {'class': 'media-heading'}):
        title_info = h3_tag.find('a')
        title.append((title_info.text.strip()))


def get_info():
    for div_tag in soup.find_all('div', {'class': 'media-body'}):
        try:
            p_tag = div_tag.find('p')
            headlines.append(p_tag.text.strip())
        except AttributeError:
            headlines.append('NO HEADLINE DATA ENTERED')


while True:
    print(url)  # here for now to make sure things work. WHEN READY TO TURN IN DELETE
    if year == 2013: # 2013 is the last year of the world history dataset        
        data = {'Date': dates, 'Title': title, 'Headline': headlines}
        world_history_df = pd.DataFrame(data)
        world_history_df['Headline'] = world_history_df['Headline'].str.replace('... ReadÂ more', '')
        world_history_df['Headline'] = world_history_df['Headline'].str.strip()
        world_history_df['Title'] = world_history_df['Title'].str.strip()

        print(world_history_df.head())
        # world_history_df.to_csv('world_history_project.csv') PUT BACK IN WHEN READY TO TURN IN PROJECT
        sys.exit()

    webpage_contents = requests.get(url).text
    soup = BeautifulSoup(webpage_contents, "lxml")
    page_num += 1
    url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
    result = soup.find('div', {'class': 'col-xs-12 pagination-container'}).find('ul').find('li',
                                                                                           {'class': 'next disabled'})

    get_dates()
    get_titles()
    get_info()

    if result is not None:
        year += 1
        page_num = 1
        url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)

    else:
        continue

'''
Transformations needed to make:  
1.  Format all the dates into one type.  If a date has date to date, remove the second date.
2.  Strip whitespace from Title and Headline columns
3.  Replace or create headers was done in the Python code. 
4.  Remove the '... ReadÂ more' from each value in the Headline column
5.  
'''

