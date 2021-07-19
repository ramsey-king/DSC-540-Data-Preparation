from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import datetime as dt

#  import numpy as np

'''
Transformations needed to make:  
1.  Create new date column (type str) converting datetime column to more readable format.
https://www.journaldev.com/23365/python-string-to-datetime-strptime
2.  Strip whitespace from Title and Headline columns (DONE)
3.  Replace or create headers was done in the Python code.  (DONE)
4.  Remove the '... ReadÂ more' from each value in the Headline column (DONE)
5.  Create a year column to be used to make a relationship between the LDS General Conference Corpus and the World 
    History Project. (DONE)
'''


year = 1942  # CHANGE BACK TO 1942 WHEN READY TO TURN IN
page_num = 1
url = 'https://worldhistoryproject.org/' + str(year) + '/page/' + str(page_num)
webpage_contents = requests.get(url).text
response = requests.get(url)
soup = BeautifulSoup(webpage_contents, "lxml")

year_column, dates, date_string, title, headlines = [], [], [], [], []


def get_dates():
    for li_tag in soup.find_all('li', {'class': 'media event'}):
        time_info = li_tag.find('time')
        dates.append(time_info.attrs['datetime'])
        #date_string.append(time_info.attrs['datetime'].dt.strftime('%b %d, %Y'))
        # dates.append(time_info.text.strip())
        year_column.append(year)


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


def make_dataset():
    data = {'Year': year_column, 'Date': dates, 'Title': title, 'Headline': headlines}
    df = pd.DataFrame(data)
    df['Headline'] = df['Headline'].str.replace('... ReadÂ more', '')
    df['Headline'] = df['Headline'].str.strip()
    df['Title'] = df['Title'].str.strip()
    return df


while True:
    if year == 2013:  # 2013 is the last year of the world history dataset
        world_history_df = make_dataset()
        print(world_history_df['Date'])
        world_history_df.to_csv('world_history_project.csv') 
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

