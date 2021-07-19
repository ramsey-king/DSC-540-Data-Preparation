import sys
import pandas as pd
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

'''
This file will pull all the general conference talks from scriptures.byu.edu into a dataframe (and later exported to 
csv for offline usage and data manipulation.)  

The url below references on the page 5532 talks from 1942 to 2021 that use the word "the", which is every talk.

The goal is to get the talk title, speaker, and date from the right window containing the search, and then using
selenium to click on the links and scrape the talk information

First I will need to figure out how to go through the right window and gather all the talk data.
'''

url = 'https://scriptures.byu.edu/#::st&&1942&2021&g&n&5532@0$the'  # n&5532 is the entire list

path_linux = "/home/ramsey/Documents/chromedriver"
driver = webdriver.Chrome(path_linux)

# path_pc = 'C:\\Users\\Ramsey\\Downloads\\chromedriver.exe'
# driver = webdriver.Chrome(path_pc)
driver.get(url)

'''
I was able to find the url that will pull the entire list of talks containing the letter a from 1942 to 2021.  The first
goal is to scrape the talk title, speaker, and date from the right window containing the list.  The first pass will be
to get all the info into a list, and the second pass will be to parse the data accordingly
'''


def get_list():
    try:
        # when running entire dataset (5532 elements), put 70 seconds as delay time
        WebDriverWait(driver, 70).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'searchresults'))
        )

        gc_list = []
        info = driver.find_elements_by_class_name('resultTitle')
        try:
            for element in info:
                gc_list.append(element.text)
        except selenium.common.exceptions.NoSuchElementException:
            gc_list.append("NO DATA FOUND")

        '''I want to get the search list first.
        Then I want to click on a talk.
        I want to get the talk text and put it in a list.
        Then I want to click on the next talk.
        And put that talk in a list, and so on..'''
        talk_list = []
        time.sleep(1)
        talks = driver.find_elements_by_class_name('grid')
        # print(len(talks))
        for talk in range(len(talks)):
            driver.find_elements_by_class_name('grid')[talk].click()
            time.sleep(1)
            paragraphs = driver.find_elements_by_class_name('gcbody')
            if not paragraphs:
                paragraphs = driver.find_elements_by_class_name('primary-article')
            if not paragraphs:
                paragraphs = driver.find_elements_by_class_name('body-block')
            for paragraph in paragraphs:
                talk_list.append(paragraph.text)
        talk_list = [i for i in talk_list if i]
        # print(talk_list)
        # print(len(gc_list))
        # print(talk_list)
        return gc_list, talk_list
    finally:
        driver.quit()


'''
def parse_components(list_to_parse):
    parsed_df = pd.DataFrame(columns=['Title', 'Speaker', 'Conf_Session', 'Source'])
    for i in range(len(list_to_parse)):
        f = filter(None, re.split(" \((?!Sam\) Wong)", list_to_parse[i]))
        filtered_list = []
        for j in f:
            filtered_list.append(j)
        f2 = filter(None, re.split(",(?! Jr.)", filtered_list[1]))

        filtered_list_2 = []
        for h in f2:
            filtered_list_2.append(h)
        filtered_list.pop()

        for k in range(len(filtered_list_2)):
            filtered_list.append(filtered_list_2[k])
        parsed_df.loc[len(parsed_df)] = filtered_list
        print(filtered_list)
    return parsed_df
    # return filtered_list
    '''


if __name__ == '__main__':
    the_list, the_talks = get_list()
    the_dict = {'List': the_list, 'Talks': the_talks}
    df = pd.DataFrame(the_dict)
    df.to_csv('talk_info2.csv')
    # final_df = parse_components(the_list)
    # final_df.to_csv('talk_info.csv')
