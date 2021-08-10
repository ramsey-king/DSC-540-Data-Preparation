import sys
import pandas as pd
import datetime as dt
import re
import requests



# Additional transfomrations to datasets for final project
def load_doctrine_and_covenants():
    # triple_combo_df = pd.read_json(
    #     '/home/ramsey/PycharmProjects/DSC-540-Data-Preparation/Final-Project/lds-scriptures-json.txt'
    # )

    triple_combo_df = pd.read_json(
        'C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\Final-Project\\lds-scriptures-json.txt'
    )

    print(triple_combo_df.info())

    doc_and_cov_df = triple_combo_df[triple_combo_df['volume_title'] == 'Doctrine and Covenants'].copy()
    print(doc_and_cov_df.info())


def world_history_process():
    world_history_df = pd.read_csv(
        'C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\Final-Project\\world_history_project.csv')
    
    # world_history_df = pd.read_csv(
    #     '/home/ramsey/PycharmProjects/DSC-540-Data-Preparation/Final-Project/world_history_project.csv'
    # )

    # strip '... Read More' from each line
    world_history_df['Headline'] = world_history_df['Headline'].str.replace('... Read more', '', regex=False)
    world_history_df['Headline'] = world_history_df['Headline'].str.strip()
    world_history_df['Title'] = world_history_df['Title'].str.strip()

    world_history_df.drop(world_history_df[world_history_df['Headline'] == 'NO HEADLINE DATA ENTERED'].index,
                          inplace=True)

    # create year column
    # some columns in the Date column have dates in the format of <DMY> to <DMY>. The second date will be dropped.
    world_history_df['Date'] = world_history_df['Date'].str.replace(' to(.*)', '', regex=True)
    world_history_df['Date'] = pd.to_datetime(world_history_df['Date'])
    world_history_df['Year'] = world_history_df['Date'].dt.year

    print(world_history_df.shape)

    # drop years earlier than 1960
    world_history_df.drop(world_history_df[world_history_df['Year'] <= 1959].index, inplace=True)

    world_history_df['Month'] = world_history_df['Date'].dt.month
    world_history_df['Year_Month'] = world_history_df['Date'].dt.to_period('M')


conference_talk_df = pd.read_csv(
    'all_talks.csv'
)
# conference_talk_df = pd.read_csv(
#     '/home/ramsey/PycharmProjects/DSC-540-Data-Preparation/all_talks.csv'
# )


def conference_talk_process():
    speaker_pattern = re.compile('\((.*?)\,')
    year_pattern = re.compile('(\d{4})')
    month_pattern = re.compile('\d{4} (Annual)')
    title_pattern = re.compile('^(.*?)\(')

    # conference_talk_df = pd.read_csv(
    #     'C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\all_talks.csv')

    # Get the speaker from the list column
    conference_talk_df['Speaker'] = conference_talk_df.List.str.extract(speaker_pattern, expand=True)
    # Get the year from the list column
    conference_talk_df['Year'] = conference_talk_df.List.str.extract(year_pattern, expand=True)
    # Set the Month column (as a string)
    conference_talk_df['Month'] = conference_talk_df.List.str.contains(month_pattern, regex=True)
    conference_talk_df['Month'] = conference_talk_df.loc[conference_talk_df.Month == False, 'Month'] = 'April'
    conference_talk_df['Month'] = conference_talk_df.loc[conference_talk_df.Month == True, 'Month'] = 'October'

    # Put the talk title into a column
    conference_talk_df['Title'] = conference_talk_df.List.str.extract(title_pattern, expand=True)

    # print(conference_talk_df.head(10))


def get_scripture_ref():
    patterns = ['(\d+ \w+ \d+\:\d+\-\d+)|', '(\d+ \w+ \d+\:\d+)|', '(\w+&\w+ \d+\:\d+)|',
                '(\w+\. \d+\:\d+\-\d+)|', '(Doctrine and Covenants \d+\:\d+)|',
                '(\w+ \d+\:\d+\–\d+)|', '(\d+ \w+ \d+\:\d+\–\d+)|', '(\w+ \d+\:\d+)']

    scripture_regex = ''.join(elem for elem in patterns)

    scripture_reference_list = []
    for i in range(len(conference_talk_df['Talks'])):
    # for i in range(10):
        match = re.findall(scripture_regex, conference_talk_df['Talks'].iloc[i])
        scripture_reference_list.append([(''.join(list(x for x in _ if x))) for _ in match])
        scripture_reference_list[i] = list(set(scripture_reference_list[i]))
    scripture_reference_list = ['; '.join(y) for y in scripture_reference_list if y]

    sr_df = pd.DataFrame(columns=['scripture_references'],
                         data=[elem for elem in scripture_reference_list])
    # print(scripture_reference_list[97])
    # print(sr_df.info())
    # print(sr_df.head())
    # sr_df.to_csv('scripture_references.csv')


    api_nephi_query = "https://api.nephi.org/scriptures/?q="

    json_data = []
    api_df =  pd.DataFrame(columns=['scripture', 'book', 'chapter', 'verse', 'text'])
    for j in range(len(scripture_reference_list)): # ENTIRE DATASET
    # for j in range(100): # TO MAKE SURE CODE WORKS
        print(j)
        try:
            the_request = requests.get(api_nephi_query+scripture_reference_list[j]).json()
            if not the_request['scriptures']:
                continue
            else:
                json_data.append(the_request)
        except ValueError:
                json_data.append({'api': {'q': 'NO DATA FOUND', 'format': 'json'},
                'scriptures': [{'scripture': 'NO DATA FOUND', 'book': 'NO DATA FOUND', 
                'chapter': 0, 'verse': 0, 'text': 'NO DATA FOUND'}]}
                )
        # finally:
        #     print(json_data[j])
    for i in range(len(json_data)):
        # print(i, type(i))
        for k in range(len(json_data[i]['scriptures'])):
            api_df = api_df.append(json_data[i]['scriptures'][k], ignore_index=True)

    # print(api_df.info())
    # print(api_df.head(20))
    api_df.to_csv('api.csv')


if __name__ == '__main__':
    # world_history_process()
    conference_talk_process()
    get_scripture_ref()
    load_doctrine_and_covenants()
