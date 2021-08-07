import sys
import pandas as pd
import datetime as dt
from better_profanity import profanity
import re


# Additional transfomrations to datasets for final project
profanity.load_censor_words()

def world_history_process():
    world_history_df = pd.read_csv(
        'C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\Final-Project\\world_history_project.csv')

    # strip '... Read More' from each line
    world_history_df['Headline'] = world_history_df['Headline'].str.replace('... Read more', '', regex=False)
    world_history_df['Headline'] = world_history_df['Headline'].str.strip()
    world_history_df['Title'] = world_history_df['Title'].str.strip()
    
    world_history_df.drop(world_history_df[world_history_df['Headline'] == 'NO HEADLINE DATA ENTERED'].index, inplace = True)
     
    # create year column
    # some columns in the Date column have dates in the format of <DMY> to <DMY>. The second date will be dropped.
    world_history_df['Date'] = world_history_df['Date'].str.replace(' to(.*)', '', regex=True)
    world_history_df['Date'] = pd.to_datetime(world_history_df['Date'])
    world_history_df['Year'] = world_history_df['Date'].dt.year

    print(world_history_df.shape)

    # drop years earlier than 1960
    world_history_df.drop(world_history_df[world_history_df['Year'] <= 1959].index, inplace = True)

    world_history_df['Month'] = world_history_df['Date'].dt.month
    world_history_df['Year_Month'] = world_history_df['Date'].dt.to_period('M')

    
def conference_talk_process():
    speaker_pattern = re.compile('\((.*?)\,')
    year_pattern = re.compile('(\d{4})')
    month_pattern = re.compile('\d{4} (Annual)')
    title_pattern = re.compile('^(.*?)\(')

    conference_talk_df = pd.read_csv(
        'C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\all_talks.csv')
    # Get the speaker from the list column
    conference_talk_df['Speaker'] = conference_talk_df.List.str.extract(speaker_pattern,expand=True)
    # Get the year from the list column
    conference_talk_df['Year'] = conference_talk_df.List.str.extract(year_pattern,expand=True)
    # Set the Month column (as a string)
    conference_talk_df['Month'] = conference_talk_df.List.str.contains(month_pattern, regex=True)
    conference_talk_df['Month'] = conference_talk_df.loc[conference_talk_df.Month == False, 'Month'] = 'April'
    conference_talk_df['Month'] = conference_talk_df.loc[conference_talk_df.Month == True, 'Month'] = 'October'

    # Put the talk title into a column
    conference_talk_df['Title'] = conference_talk_df.List.str.extract(title_pattern,expand=True)

    print(conference_talk_df.head(10))

if __name__ == '__main__':
    
    # world_history_process()
    conference_talk_process()