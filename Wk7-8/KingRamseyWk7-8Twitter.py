import twitter
import pandas as pd
api = twitter.Api(consumer_key='D8KM23T3iFpwLO8OgQihpSMAX',
    consumer_secret='HEkmbBUDVtZLTuWq2guji0IRnwQmjHLCI2IJtgH7ZSdT3ju6LW',
    access_token_key='1419712533322153985-QjB21Rd8UThAzMFHngjRp7iYaoHZet',
    access_token_secret='XN99oI69OKRgz7Dy4PkR0uc5Di9VxbcOq8hsceh98SJ5S')

# print(api.VerifyCredentials())

# Website to Twitter tutorial
# 'https://www.sitepoint.com/how-to-create-a-twitter-app-and-api-interface-via-python/'

bellevue_search = api.GetSearch(term='(%23bellevueuniversity)', since='2000-01-01', count=1000)
bellevue_search += api.GetSearch(term='Bellevue University', since='2000-01-01', count=1000)
# print(len(bellevue_search))
bell_dict = {'bellevue':bellevue_search}
df = pd.DataFrame(bell_dict)
df.to_excel('bellevue.xlsx')

data_science_search = api.GetSearch(term='(%23datascience)', since='2000-01-01', count=1000)
data_science_search += api.GetSearch(term='data science', since='2000-01-01', count=1000)
# print(len(data_science_search))
ds_dict = {'data science':data_science_search}
df = pd.DataFrame(ds_dict)
df.to_excel('ds.xlsx')