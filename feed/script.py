from flask import request
from pymongo import MongoClient
from threading import Thread
import re

try:
    from .conf import AUTH_TOKEN
except ImportError:
    from conf import AUTH_TOKEN

client = MongoClient('localhost', 27017)
URL_REGEX = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

import json
import requests
from requests.exceptions import HTTPError

url="https://api.twitter.com/2/tweets?ids="
headers = '&expansions=referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld&user.fields=username,verified'
header = {
    'Authorization': 'Bearer ' + AUTH_TOKEN,
    'expansions':'referenced_tweets.id.author_id',
    'tweet.fields':'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
    'user.fields':'username,verified'
}

def get_saves():
    return client.feed.tuites_bookmarks.find()

def get_more_info():
    for i,t in enumerate(client.feed.tuites_bookmarks.find()):
        if t.get("includes") is None:
            # breakpoint()
            response = requests.get(
                url+t['id']+headers,
                headers={'Authorization': 'Bearer ' + AUTH_TOKEN}
                )
            if response.ok:
                # breakpoint()
                print(i)
                print(response.json())
                client.feed.tuites_bookmarks.update_one(t,{'$set':response.json()})
            else:
                print(i,
                    response,
                    response.text
                    )
            
def get_link_in_text():
    
        # print("substituição link", link)

    def get_(urls:list,t):
        novas_urls=[]
        try:
            for url in urls:
                if not "//t.co" in url: continue
                novas_urls.append(requests.get(url).url)
        except HTTPError as HE:
            print("IMPLEMNT******************",str(HE))
            client.feed.tuites_bookmarks.update_one(t,{'$unset':{"last_link":""}})
            # breakpoint()
            print("links ",urls," deletadas")

        client.feed.tuites_bookmarks.update_one(t,{'$set':{"last_link":novas_urls}})
        # breakpoint()
        print(i,t['text'],novas_urls)

    for i,t in enumerate(client.feed.tuites_bookmarks.find()):
        
        text = t.get('text','')

        if matches:=re.findall(URL_REGEX,text):
            if not t.get("last_link",False) or any(filter(lambda x:"//t.co" in x,t.get("last_link",[]))):
                for url in matches:
                    if "//t.co" in url:

                        Thread(target=get_,args=[matches,t]).start()
                # continue
                # break
            # breakpoint()
            print("*** link encontrado",matches)


if __name__=='__main__':
    get_link_in_text()