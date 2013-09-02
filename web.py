"""
Module for the Colorado Alliance of Research Libraries Metadata 2013
Presentation
"""
__author__ = "Jeremy Nelson"

import datetime
import json
import os
import redis

from bottle import abort, request, route, run, static_file
from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import FlupFCGIServer

PROJECT_ROOT = os.path.split(os.path.abspath(__name__))[0]

PRESENTATION_INFO = json.load(open(os.path.join(PROJECT_ROOT,
                                                'slides.json'),
                                   'rb'))
SLIDES = PRESENTATION_INFO.get('slides')

DEMO_REDIS = redis.StrictRedis()

@route('/metadata-day-2013/assets/<type_of:path>/<filename:path>')
def send_asset(type_of,filename):
    local_path = os.path.join(PROJECT_ROOT,
                              "assets",
                              type_of,
                              filename)
    if os.path.exists(local_path):
        return static_file(filename,
			   root=os.path.join(PROJECT_ROOT,
                                             "assets",
                                             type_of))
    

@route("/metadata-day-2013/")
def index():
    record_sets = {}
    return template('index',
                    category='home',
                    slides=SLIDES)
FLUP = False
if FLUP is True:
    run(server=FlupFCGIServer,
        host='0.0.0.0',
        port=8014)
else:
    run(host='0.0.0.0', 
        port=8014, 
        reloader=True)
