from flask import Flask, abort, jsonify,render_template, request
from .script import get_saves
import requests
import opengraph_py3 as  opengraph

app = Flask(__name__)

@app.get("/teste")
def test_client():
    return 'Testing, Flask!'

@app.get("/")
def index():
    saves = get_saves()
    return render_template("index.html",saves=saves)

@app.post("/preview/")
def preview():

    # breakpoint()
    link = request.get_json()['link']
    # request.json
    if not link: return abort(404)
    
    try:
        og = opengraph.OpenGraph(url=link)
    except:
        return "",404
    
    # breakpoint()
    return jsonify(og )
    

# @app.post("/preview/")
# def preview():
#     link = request.get_json()['link']
#     # request.json
#     if not link: return abort(404)
    
#     # breakpoint()

#     response = requests.post(
#         "https://api.peekalink.io/",
#         headers={"X-API-Key": "31ad129a-67d6-4c7b-a98b-1e4fc9113d5d"},
#         data={"link": link}
#     )
#     if response.ok :
#         # breakpoint()
#         return jsonify( response.json() )
#     print(response,response.text)
#     return abort(403)
#     # breakpoint()




if __name__ == "__main__":
    app.run()


"""
AAAAAAAAAAAAAAAAAAAAAEFwUwEAAAAAXWo9rN3J%2BEEs3GlzxSQI5GOdz4s%3DoNuSxMbZeartsdmgJvbxT3hyxZvSyCR1y7JltGrcVOzj5QTAUv
"""