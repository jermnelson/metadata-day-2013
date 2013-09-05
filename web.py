"""
Module for the Colorado Alliance of Research Libraries Metadata 2013
Presentation

Copyright (C) 2013 Jeremy Nelson 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = "Jeremy Nelson"

import argparse
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

FLUP = False

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
    

@route("/metadata-day-2013/bibframe.html")
def bibframe():
    return template('bibframe',
                    category='slides',
                    next_slide=SLIDES[2],
                    slide=SLIDES[1],
                    slides=SLIDES)

@route("/metadata-day-2013/bibframe-adr.html")
def bibframe():
    return template('bibframe-adr',
                    category='slides',
                    slide=SLIDES[-1],
                    slides=SLIDES)


@route("/metadata-day-2013/linked-data.html")
def linked_data():
    return template('linked-data',
                    category='slides',
                    next_slide=SLIDES[1],
                    slide=SLIDES[0],
                    slides=SLIDES)

@route("/metadata-day-2013/marc-to-bibframe.html")
def marc_to_bibframe():
    return template('marc-bibframe',
                    category='slides',
                    next_slide=SLIDES[3],
                    slide=SLIDES[2],
                    slides=SLIDES)

@route("/metadata-day-2013/mods-to-bibframe.html")
def mods_to_bibframe():
    return template('mods-bibframe',
                    category='slides',
                    next_slide=SLIDES[4],
                    slide=SLIDES[3],
                    slides=SLIDES)
                    

@route("/metadata-day-2013/resources.html")
def resources():
    return template('resources',
                    category='home',
                    slides=SLIDES)
    


@route("/metadata-day-2013/")
def index():
    return template('index',
                    category='home',
                    slides=SLIDES)


parser = argparse.ArgumentParser(
    description='Run ADR Metadata Day 2013 Presentation')
parser.add_argument('mode',
                    help='Run in either prod (production) or dev (development)')

mode = parser.parse_args().mode
if mode == 'prod': 
    run(server=FlupFCGIServer,
        host='0.0.0.0',
        port=9010)
elif mode == 'dev':
    run(host='0.0.0.0', 
        port=9010,
        debug=True,
        reloader=True)
else:
    print("ERROR unknown run mode {0}".format(mode))
