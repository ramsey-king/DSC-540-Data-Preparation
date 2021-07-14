import requests
import sys
import pandas as pd
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
talk_num = 2
url = 'https://scriptures.byu.edu/#:t' + str(talk_num)


path_linux = "/home/ramsey/Documents/chromedriver"
driver = webdriver.Chrome(path_linux)
driver.get(url)
# print(driver.title)
driver.implicitly_wait(10)

# search = driver.find_element_by_id('centercolumn')

try:
    webpage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "centercolumn"))
    )

    # print(webpage.text)
    talk_header_info = webpage.find_elements_by_class_name('gchead')
    for element in talk_header_info:
        print(element.text)

    print(webpage.find_element_by_class_name('gctitle').text)

    paragraphs = webpage.find_elements_by_class_name("gcbody")
    for paragraph in paragraphs:
        print(paragraph.text)
finally:
    driver.quit()


# if __name__ == '__main__':
