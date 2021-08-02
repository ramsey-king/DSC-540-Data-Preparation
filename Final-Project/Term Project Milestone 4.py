import pandas as pd
import re
import requests

talk_data = pd.read_csv('C:\\Users\\Ramsey\\VSCodeProjects\\DSC-540-Data-Preparation\\Final-Project\\talk_info2.csv', sep=",")

scripture_regex = '(\d+ \w+ \d+\:\d+\-\d+)|(\w+ \d+\:\d+)|(\d+ \w+ \d+\:\d+)|(\w+&\w+ \d+\:\d+)|(\w+\. \d+\:\d+\-\d+)'

# match = re.findall(scripture_regex, talk_data['Talks'].iloc[0])
# new = [(''.join(list(x for x in _ if x))) for _ in match]
# print(new)

scripture_reference_list = []
for i in range(len(talk_data['Talks'])):
    match = re.findall(scripture_regex, talk_data['Talks'].iloc[i])
    scripture_reference_list.append([(''.join(list(x for x in _ if x))) for _ in match])
scripture_reference_list = ['; '.join(y) for y in scripture_reference_list if y]
# print(scripture_reference_list)

api_nephi_query = "https://api.nephi.org/scriptures/?q="

json_data = []
# for j in range(len(scripture_reference_list)): ENTIRE DATASET
for j in range(10): # TO MAKE SURE CODE WORKS
    json_data.append(requests.get(api_nephi_query+scripture_reference_list[j]).text)


# print(json_data)

api_df = pd.DataFrame(columns=['json'])

# for i in range(len(scripture_reference_list)):
for i in range(10): # TO MAKE SURE CODE WORKS
    api_df.loc[i] = [json_data[i]]

print(api_df.info)

# I NEED TO EXTRACT THE DICTIONARY KEYS INTO COLUMNS OF MY API_DF FOR MY TRANSFORMATIONS.