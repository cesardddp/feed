from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)


with open("tuites.json") as f:
    
    client.feed.tuites_bookmarks.insert_many(
        json.loads(
            f.read()
        )
    )
