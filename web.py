import logging, unittest
from flask import Flask, render_template, url_for
from werkzeug.contrib.cache import SimpleCache
from suggestor import suggest
from storage import PlaceStorage as Storage
import requests
import json
import os

app = Flask(__name__)
cache = SimpleCache()

@app.route('/services/suggest/<target_text>')
def get_similar_places(target_text):
    logging.info('Searching for place <{0}>'.format(target_text))
    return json.dumps(suggest(target_text))
    
@app.route('/services/info/<place_name>')
def get_place_info(place_name):
    logging.info('Getting place <{0}> info'.format(place_name))
    response = cache.get(place_name)
    if not response:
        response = ''
        place = Storage().get_place(place_name)
        if place:
            name,info,_,_ = place
            response = json.dumps({'name':name,'info':info})
            cache.set(place_name, response, timeout=3600)
    return response
        
@app.route('/')
def search_home():
    return render_template('search.html')
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)