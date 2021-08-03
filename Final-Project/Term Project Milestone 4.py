import pandas as pd
import re
import requests

talk_data = pd.read_csv('C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\Final-Project\\talk_info2.csv', sep=",")

scripture_regex = '(\d+ \w+ \d+\:\d+\-\d+)|(\w+ \d+\:\d+)|(\d+ \w+ \d+\:\d+)|(\w+&\w+ \d+\:\d+)|(\w+\. \d+\:\d+\-\d+)'

scripture_reference_list = []
for i in range(len(talk_data['Talks'])):
    match = re.findall(scripture_regex, talk_data['Talks'].iloc[i])
    scripture_reference_list.append([(''.join(list(x for x in _ if x))) for _ in match])
scripture_reference_list = ['; '.join(y) for y in scripture_reference_list if y]

api_nephi_query = "https://api.nephi.org/scriptures/?q="

json_data = []
api_df =  pd.DataFrame(columns=['scripture', 'book', 'chapter', 'verse', 'text'])
# for j in range(len(scripture_reference_list)): ENTIRE DATASET
for j in range(10): # TO MAKE SURE CODE WORKS
    the_request = requests.get(api_nephi_query+scripture_reference_list[j]).json()
    if not the_request['scriptures']:
        continue
    else:
        json_data.append(the_request)
    
for i in range(len(json_data)):
    for k in range(len(json_data[i]['scriptures'])):
        api_df = api_df.append(json_data[i]['scriptures'][k], ignore_index=True)

print(api_df.head(20))
