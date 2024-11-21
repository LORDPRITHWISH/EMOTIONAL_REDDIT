import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json

def request (link):
    print("link is ",link)
    link+='.json?limit=100&sort=hot&t=all'
    res=requests.get(link)

    with open('rawfull.json','w',encoding='utf-8') as sour :
        sour.write(json.dumps(res.json(),indent=4))

    print(res.json())
    aft = res.json()['data']['after']
    json_data = res.json()
    # print("data is ",json_data)
    while aft:
        # print("data is ",json_data)
        res=requests.get(link+f'&after={aft}')
        if res.status_code != 200:
            break
        json_data['data']['children'].extend(res.json()['data']['children'])
        aft = res.json()['data']['after']


    if res.status_code == 200:
        print("Data fetched successfully")
        print("data type is ",type(json_data))
        return json_data
    else:
        print(f"Failed to fetch data. Status code: {res.status_code}")
