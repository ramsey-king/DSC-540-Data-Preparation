import requests
import sys
import pandas as pd
import datetime as dt
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#  import numpy as np

'''
This file will pull all the general conference talks from scriptures.byu.edu into a dataframe (and later exported to 
csv for offline usage and data manipulation.)  

Currently what I have working is I am able to pull in the first 719 talks. (/#:t1 -- /#:t719). 

I also need to figure out how to pull in the date from the "talklabel" div id and add that to the dataframe as a date.
I can pull it in as is, and then manipulate it later. DONE

I also need to get the scripture references used in the talk into a list to be used for later manipulation and add that
to a column in the data frame. DONE

Finally, and maybe the most difficult portion of this will be to figure out the nomenclature of the talks that aren't
just numbers.  For example, /#:t71a goes to another talk, as does /#:t1a
'''

# https://scriptures.byu.edu/#:t2
talk_num = 719
url = 'https://scriptures.byu.edu/#:t' + str(talk_num)

path_linux = "/home/ramsey/Documents/chromedriver"
driver = webdriver.Chrome(path_linux)

# path_pc = 'C:\\Users\\Ramsey\\Downloads\\chromedriver.exe'
# driver = webdriver.Chrome(path_pc)
driver.get(url)
# print(driver.title)


# search = driver.find_element_by_id('centercolumn')
talk_title, talk_label, speaker, position, bibliography, scripture_reference, talk_contents = [], [], [], [], [], [], []


def get_talk():
    try:
        webpage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "centercolumn"))
        )

        # print(webpage.text)
        time.sleep(1.5)

        try:
            talk_label.append(webpage.find_element_by_id('talklabel').text)
        except selenium.common.exceptions.NoSuchElementException:
            talk_label.append("NO DATA FOUND")

        talk_header_info = webpage.find_elements_by_class_name('gchead')
        for element in talk_header_info:
            try:
                talk_title.append(webpage.find_element_by_class_name('gctitle').text)
            except selenium.common.exceptions.NoSuchElementException:
                talk_title.append("NO DATA FOUND")

            try:
                speaker.append(webpage.find_element_by_class_name('gcspeaker').text)
            except selenium.common.exceptions.NoSuchElementException:
                speaker.append("NO DATA FOUND")

            try:
                position.append(webpage.find_element_by_class_name('gcspkpos').text)
            except selenium.common.exceptions.NoSuchElementException:
                position.append("NO DATA FOUND")

            try:
                bibliography.append(webpage.find_element_by_class_name('gcbib').text)
            except selenium.common.exceptions.NoSuchElementException:
                bibliography.append("NO DATA FOUND")

        paragraphs = webpage.find_elements_by_class_name("gcbody")
        for paragraph in paragraphs:
            talk_contents.append(paragraph.text)

        citations = webpage.find_elements_by_class_name('citation')
        reference = []
        for citation in citations:
            reference.append(citation.text)
            print(reference)

        # print(len(talk_title), len(talk_contents))
        scripture_reference.append(reference)
        print(scripture_reference)
    finally:
        driver.quit()


def make_dataset():
    data = {'Title': talk_title, 'Date_Info': talk_label, 'Speaker': speaker, 'Position': position,
            'Bibliography': bibliography, 'Scripture_References': scripture_reference, 'Talk': talk_contents}
    df = pd.DataFrame(data)
    return df


while True:
    # print(url)  # here for now to make sure things work. WHEN READY TO TURN IN DELETE
    if talk_num == 721:  # it appears that this pattern only works for the first 720.  There are 2150
        # t720 = Hugh B Brown, October 1967, The Profile of a Prophet
        gc_df = make_dataset()
        gc_df.to_csv('gctest.csv')
        print(gc_df)
        sys.exit()

    get_talk()
    talk_num += 1
    url = 'https://scriptures.byu.edu/#:t' + str(talk_num)
    # driver = webdriver.Chrome(path_pc)
    driver = webdriver.Chrome(path_linux)
    driver.get(url)


# if __name__ == '__main__':
