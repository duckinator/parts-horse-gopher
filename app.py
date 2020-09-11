#!/usr/bin/env python3

import os
from urllib.request import urlopen
import json
from flask import Flask, request
from flask_gopher import GopherExtension, GopherRequestHandler


ROOT_DIR = os.path.dirname(__file__)

app = Flask(__name__, static_url_path='')
app.config.from_pyfile('parts-horse.cfg')
gopher = GopherExtension(app)


def json_get(path):
    """Fetch API endpoints from Parts Horse."""
    if path[0] == '/':
        path = path[1:]
    result_text = urlopen(f'https://parts.horse/{path}').read().decode()
    return json.loads(result_text)


@app.route('/', defaults={'query': None})
def index(query):
    if query is None:
        query = request.environ['SEARCH_TEXT']

    if query:
        return search(query)
    return gopher.render_menu_template('index.gopher')


@app.route('/parts')
def parts_list():
    return gopher.render_menu_template('parts-list.gopher', page=json_get('parts.json'))

@app.route('/parts/<part>')
def parts(part):
    if part is None:
        part = request.environ['SEARCH_TEXT']
    page = json_get('parts/{part}.json')
    return gopher.render_menu_template('part.gopher', page=page)


@app.route('/search', defaults={'query': None})
@app.route('/search/<query>')
def search(query):
    if query is None:
        query = request.environ['SEARCH_TEXT']
    page = json_get(f'search?q={query}')
    return gopher.render_menu_template('search.gopher', page=page)


if __name__ == '__main__':
    #app.run('127.0.0.1', 7070, request_handler=GopherRequestHandler)
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        threaded=app.config['THREADED'],
        processes=app.config['PROCESSES'],
        request_handler=GopherRequestHandler
    )
