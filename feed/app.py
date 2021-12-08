import re
from flask import Flask, abort, jsonify,render_template, request
from .script import get_saves,client,URL_REGEX
import requests
import opengraph_py3 as  opengraph
from flask_caching import Cache
import logging

config = {
    # "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    'CORS_HEADERS' : 'Content-Type'
}
## APP FACTORY #######
# cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# app = Flask(__name__)
# cache.init_app(app)
######################

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)

@app.get("/teste")
def test_client():
    return 'Testing, Flask!'

@app.get("/")
def index():
    saves = get_saves()
    # return render_template("teste.html")
    return render_template("index.html",saves=saves)

@app.get("/preview")
@app.get("/preview/<id>")
@cache.cached(timeout=9999999,query_string=True)
def preview(id=""):

    # link = request.json['link']
    id = request.args.get('id')

    # request.json
    if not id:
        return abort(404)
    
    tuite = client.feed.tuites_bookmarks.find_one({'id':id})
    matches = re.findall(URL_REGEX,tuite['text'])

    try:
        print("requesting")
        og = opengraph.OpenGraph(
            html=requests.get(tuite['last_link'][-1]).text
        )
    except:
        if matches[-1] is None:
            return '{}'
            
        og = opengraph.OpenGraph(
            html=requests.get(matches[-1]).text
        )
        return "",404
    
    return jsonify(og)
    

# @app.post("/preview/")
# def preview():
#     link = request.get_json()['link']
#     # request.json
#     if not link: return abort(404)
    

#     response = requests.post(
#         "https://api.peekalink.io/",
#         headers={"X-API-Key": "31ad129a-67d6-4c7b-a98b-1e4fc9113d5d"},
#         data={"link": link}
#     )
#     if response.ok :
#         return jsonify( response.json() )
#     print(response,response.text)
#     return abort(403)




if __name__ == "__main__":
    app.run()


"""
AAAAAAAAAAAAAAAAAAAAAEFwUwEAAAAAXWo9rN3J%2BEEs3GlzxSQI5GOdz4s%3DoNuSxMbZeartsdmgJvbxT3hyxZvSyCR1y7JltGrcVOzj5QTAUv
"""