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

url = 'https://scriptures.byu.edu/#::st&&1961&2015&g&n&4037@0$the'  # n&5532 is the entire list

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
        WebDriverWait(driver, 60).until(
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
        time.sleep(0.85)
        talks = driver.find_elements_by_class_name('grid')
        # print(len(talks))
        for talk in range(len(talks)):
            driver.find_elements_by_class_name('grid')[talk].click()
            time.sleep(1)
            try:
                paragraphs = driver.find_elements_by_class_name('gcbody')
                if not paragraphs:
                    paragraphs = driver.find_elements_by_class_name('primary-article')
                if not paragraphs:
                    paragraphs = driver.find_elements_by_class_name('body-block')
                if not paragraphs:
                    paragraphs = driver.find_elements_by_id('primary')
                for paragraph in paragraphs:
                    talk_list.append(paragraph.text)
                    print("talk list len:", len(talk_list), "gc list len:", len(gc_list))
            except selenium.common.exceptions.StaleElementReferenceException:
                talk_list.append("NO DATA FOUND")
        talk_list = [i for i in talk_list if i]
        # print(talk_list)
        print("talk list len:", len(talk_list), "gc list len:", len(gc_list))
        # print(talk_list)
        return gc_list, talk_list
    finally:
        driver.quit()


# Put the two csv's together to have one csv with the header info and the talk text
def combine_csv(csv1, csv2):
    pass



if __name__ == '__main__':
    the_list, the_talks = get_list()
    the_talk_info_dict = {'List': the_list}
    the_talk_text_dict = {'Talks': the_talks}
    df = pd.DataFrame(the_talk_info_dict)
    df.to_csv('talk_info_dict.csv')
    df = pd.DataFrame(the_talk_text_dict)
    df.to_csv('the_talk_text_dict.csv')
    # final_df = parse_components(the_list)
    # final_df.to_csv('talk_info.csv')
