import twitter
import matplotlib.pyplot as plt
import numpy as np

api = twitter.Api(consumer_key='D8KM23T3iFpwLO8OgQihpSMAX',
    consumer_secret='HEkmbBUDVtZLTuWq2guji0IRnwQmjHLCI2IJtgH7ZSdT3ju6LW',
    access_token_key='1419712533322153985-QjB21Rd8UThAzMFHngjRp7iYaoHZet',
    access_token_secret='XN99oI69OKRgz7Dy4PkR0uc5Di9VxbcOq8hsceh98SJ5S')

# print(api.VerifyCredentials())

def process_twitter_info(search_term):
    hash_string = '(%23' + search_term.replace(" ", "") + ')'
    api_pull = api.GetSearch(term=search_term)
    api_pull += api.GetSearch(term=hash_string)
    dict_to_parse = {'main_key': api_pull}
    # Loop through all elements and convert them to dictionary objects
    for i in range(len(dict_to_parse['main_key'])):
        dict_to_parse['main_key'][i] = dict_to_parse['main_key'][i].AsDict()
    
    return dict_to_parse

def get_hashtag_list(info_as_dict): # Use 'Bellevue University' and 'Data Science'
    tag_list = []    
    # puts all hashtags into a list (lowercase to eliminate duplicates)
    for i in range(len(info_as_dict['main_key'])):
        for j in range(len(info_as_dict['main_key'][i]['hashtags'])):
            tag_list.append(",".join(list(info_as_dict['main_key'][i]['hashtags'][j].values())).lower())

    return tag_list

def make_bar_chart(bar_chart_data):
    items, counts = np.unique(bar_chart_data, return_counts=True)
    plt.bar(items, counts)
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show()

def scatter_plot_lists(twitter_search):
    d = process_twitter_info(twitter_search)
    favorite_count_list, hashtag_count_list = [], []    
    
    for i in range(len(d['main_key'])):
        favorite_count_list.append(d['main_key'][i].get('favorite_count'))
        hashtag_count_list.append(len(d['main_key'][i].get('hashtags')))
    # change None's to 0's
    conv = lambda i : i or 0
    favorite_count_list = [conv(i) for i in favorite_count_list]
    return favorite_count_list, hashtag_count_list
    
def make_scatter_plot(scatter_x, scatter_y):
    plt.scatter(scatter_x, scatter_y)
    plt.xlabel('Favorite Count')
    plt.ylabel('Hashtag Count')
    plt.title('Favorite Count vs. Hashtag Count')
    plt.show()

def make_pie_chart(chart_list):
    b_items, b_counts = np.unique(chart_list, return_counts=True)
    plt.pie(b_counts, labels=b_items)
    plt.title('Pie Chart of hashtags')
    plt.show()
   

if __name__ == '__main__':
    
    bellevue_list = process_twitter_info('Bellevue University')
    tag_list = get_hashtag_list(bellevue_list)
    make_bar_chart(tag_list)

    x, y = scatter_plot_lists('Data Science')
    make_scatter_plot(x, y)

    make_pie_chart(tag_list)
