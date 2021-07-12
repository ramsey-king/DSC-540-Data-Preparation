from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import datetime as dt

#  import numpy as np

'''
This file will pull all the general conference talks from scriptures.byu.edu into a dataframe (and later exported to 
csv for offline usage and data manipulation.)  
'''

'''
Can we pull and print a talk from the citation index using beautiful soup?
data we need to pull from talk website: div id = 'talklabel', class = 'visiblelabel multiline_info'.  This containes
the date when the talk was given

For title - div class='gchead' p class=gctitle.text

To find information by pulling a div id:
https://stackoverflow.com/questions/2136267/beautiful-soup-and-extracting-a-div-and-its-contents-by-id
'''
# https://scriptures.byu.edu/#:t2
talk_num = 1
url = 'https://scriptures.byu.edu/#:t' + str(talk_num)
webpage_contents = requests.get(url).text
repsonse = requests.get(url)
soup = BeautifulSoup(webpage_contents, 'lxml')

for para in soup.find_all("p"):
    print(para.get_text())

def get_contents(main_tag, main_class, info_tag, info_class):
    info_list = []
    for tag in soup.find_all(main_tag, {'class': main_class}):
        info = tag.find(info_tag, {'class': info_class})
        info_list.append(info.text.strip())
    return info_list


if __name__ == '__main__':
    test_list = get_contents('div', 'gchead', 'p', 'gcspeaker')
    print(test_list)