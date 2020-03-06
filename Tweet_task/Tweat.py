import json
import os
import subprocess
import time
from collections import Counter, OrderedDict
from urllib.parse import urlparse
import nltk
import requests
import validators

os.chdir(os.path.dirname(os.path.realpath(__file__)))


def process_tweet(tweet):
    words = tweet.split()
    words = nltk.pos_tag(words)
    words = [i[0] for i in words if (i[1] not in (
        'PRP', 'PRP$', 'TO', 'IN', 'CC', 'DT'))]
    tokens = words.copy()
    words2 = []
    words = []
    for i in tokens:
        if validators.url(i):
            words.append(i)
        else:
            words2.append(i)
    words2_length = len(set(words2))
    words2_dict = dict(Counter(words2))
    words2_dict = OrderedDict(
        sorted(words2_dict.items(), key=lambda x: x[1], reverse=True)).items()
    words2_dict = list(words2_dict)[:10]
    url_count = len(words)
    try:
        domains = [urlparse(requests.head(i, allow_redirects=True).url).netloc for i in words]
    except BaseException as e:
        print(e)
        return 1, None
    domains = dict(Counter(domains))
    domains = OrderedDict(
        sorted(domains.items(), key=lambda x: x[1], reverse=True)).items()
    domains = list(domains)
    if len(domains) == 0:
        domains = "No_URLs"
    return url_count, domains, words2_length, words2_dict


while True:
    try:
        data = {}
        users = []
        items = []
        time.sleep(60)
        content = subprocess.getoutput('cat tweetsdata*').splitlines()
        content = [json.loads(i) for i in content if len(i) != 0]
        for i in content:
            user = i['user']
            text = i['text']
            users.append(user)
            data[user] = data.get(user, "") + ' ' + text
        for i, j in dict(Counter(users)).items():
            items.append([i, data[i], j])
        for i in items:
            tweet_string = i[1]
            i.extend(process_tweet(tweet_string))
        print('-' * 145)
        print(
            'User | No._of_tweets_from_user_in_last_5_min | No._of_links_in_user_tweets | (Order_of_resolved_domains_sorted_by_count_descending, count) | Total_no._of_unique_words_in_tweet | (Top_10_occurring_words_sorted_descending, count)')
        print('-' * 145)
        for i in items:
            print(i[0].ljust(15)+' | ', ' | '.join([str(j)
                                                    for j in i[2:]]), end='\n\n')
        print(len(items), 'users in last 5 minutes')
        print('#'*145)
    except KeyboardInterrupt:
        os.system('pkill -9 python')
    except BaseException as e:
        print(e)