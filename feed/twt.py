import json
from time import sleep
import requests
from conf import AUTH_TOKEN
# from multiprocessing import Th
from threading import Thread

# tuites = open("tuites.josn",'w')

def get_saves():
    return json.loads(
        open("saves.json").read()
    )

header = {'Authorization': 'Bearer ' + AUTH_TOKEN}

url = 'https://api.twitter.com/2/tweets/'

def get_tuite(id):
    global header
    response = requests.get(url+id, headers=header)
    with open("tuites.json",'a') as tuites:
        tuites.write(
            ","+json.dumps(response.json())
        )
    return response

with open("tweets.csv") as f:
    tréds = []
    for tuite in f.readlines():
        id = tuite.split("/")[-1].strip().replace(",,","")
        # tréd = Thread(
        #     target=get_tuite,args=[id,],name=id
        # )
        target=get_tuite(id)#,name=id
        # breakpoint()
        if not target.ok:
            breakpoint()
        sleep(0.3)
        # tréd.start()
        # tréds.append(tréd)

    boleano = True
    for t in tréds:
        t.join()
        if boleano:
            breakpoint()
            boleano=False


