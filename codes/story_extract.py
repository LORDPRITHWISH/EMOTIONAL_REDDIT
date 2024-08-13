import json
import demoji
from codes.json_get import request
from codes.sentiment import analyze_sentiment
import datetime

def extract(raw_json_txt) :
    # with open('tempo/rawfull.json','r',encoding='utf-8') as sour :
    #     raw_json_txt=sour.read()

    # children_cards= json.loads(raw_json_txt)['data']['children']
    # print(raw_json_txt)
    children_cards= raw_json_txt['data']['children']
    # print(*children_cards,sep='\n'*5)

    # for i in children_cards :
    #     i=i['data']
    #     i['selftext']=i['selftext'].replace('\n',' ')
    #     i['selftext']=i['selftext'].replace('\r',' ')
    #     i['selftext']=demoji.replace( i['selftext'], '')
    #     print(i['subreddit'],i['selftext'],"\n\n")

# Convert the Unix timestamp to a datetime object

    # "after": "t3_1epxiu6",

    data=[
            {
                "Subreddit": i['data']['subreddit'],
                "Title": i['data']['title'],
                "Selftext": i['data']['selftext'],
                "Upvote Ratio": i['data']['upvote_ratio'],
                "Author": i['data']['author'],
                "Time": datetime.datetime.fromtimestamp(i['data']['created'], datetime.timezone.utc).isoformat(),
                "Sentiment": analyze_sentiment(i['data']['selftext'],)
            }
            for i in children_cards if i['data']['selftext']!=""
        ]
    
    # print(data)
    return data


    # children_cards=children_cards[1:]
    # for i in children_cards :
    #     i=i['data']
    #     i['selftext']=i['selftext'].replace('\n',' ')
    #     i['selftext']=i['selftext'].replace('\r',' ')
    #     i['selftext']=demoji.replace( i['selftext'], '')
    #     with open('tempo/story.txt','a') as sour :
    #         sour.write(f'{i['subreddit']}#####{i['selftext']}\n')

def getstory(link) :
    return extract(request(link))
