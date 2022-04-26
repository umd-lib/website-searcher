import json
import logging
import os
import sys
import json
import urllib.parse
import requests

import furl
from flask import Flask, Response, request
from dotenv import load_dotenv
from waitress import serve
from paste.translogger import TransLogger

# Searcher to search Google Programmable Search Engine and return results
# in the Quick Search format.
#
# See https://developers.google.com/custom-search/v1/introduction

# Add any environment variables from .env
load_dotenv('../.env')

# Get environment variables
env = {}
for key in ('WEBSITE_SEARCHER_URL', 'WEBSITE_SEARCHER_API_KEY',
            'WEBSITE_SEARCHER_ENGINE_ID', 'WEBSITE_SEARCHER_NO_RESULTS_LINK',
            'WEBSITE_SEARCHER_MODULE_LINK'):
    env[key] = os.environ.get(key)
    if env[key] is None:
        raise RuntimeError(f'Must provide environment variable: {key}')

search_url = furl.furl(env['WEBSITE_SEARCHER_URL'])
api_key = env['WEBSITE_SEARCHER_API_KEY']
engine_id = env['WEBSITE_SEARCHER_ENGINE_ID']
no_results_link = env['WEBSITE_SEARCHER_NO_RESULTS_LINK']
module_link = env['WEBSITE_SEARCHER_MODULE_LINK']

debug = os.environ.get('FLASK_ENV') == 'development'

logging.root.addHandler(logging.StreamHandler())

loggerWaitress = logging.getLogger('waitress')
logger = logging.getLogger('website-searcher')

if debug:
    loggerWaitress.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    # from http.client import HTTPConnection
    # HTTPConnection.debuglevel = 1
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
else:
    loggerWaitress.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)

logger.info("Starting the website-searcher Flask application")

endpoint = 'website-search'


# Start the flask app, with compression enabled
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def root():
    return {'status': 'ok'}


@app.route('/ping')
def ping():
    return {'status': 'ok'}


@app.route('/search')
def search():

    # Get the request parameters
    args = request.args
    if 'q' not in args or args['q'] == "":
        return {
            'endpoint': endpoint,
            'error': {
                'msg': 'q parameter is required',
            },
        }, 400
    query = args['q']

    per_page = 3
    if 'per_page' in args and args['per_page'] != "":
    	per_page = args['per_page']

    page = 0
    if 'page' in args and args['page'] != "" and args['page'] != "%":
    	page = args['page']

    start_index = 1 + int(page) * int(per_page)

    # Execute the Google search
    params = {
        'q': query,  # query
        'key': api_key,
        'cx': engine_id,
        'num': per_page,  # number of results
        'start': start_index,  # starting at this result (1 is the first result)
    }

    try:
        response = requests.get(search_url.url, params=params)
    except Exception as err:
        logger.error(f'Error submitting search: {err}')

        return {
            'endpoint': endpoint,
            'error': {
                'msg': f'Error submitting search',
            },
        }, 500

    if response.status_code != 200:
        logger.error(f'Received {response.status_code} when submitted {query=}')

        return {
            'endpoint': endpoint,
            'error': {
                'msg': f'Received {response.status_code} when submitted {query=}',
            },
        }, 500

    data = json.loads(response.text)

    # Gather the search results into our response
    results = []
    response = {
        'endpoint': endpoint,
        'query': query,
        "per_page": str(per_page),
        "page": str(page),
        "total": int(data['searchInformation']['totalResults']),
        "module_link": module_link.replace('{query}',
                                           urllib.parse.quote_plus(query)),
        "no_results_link": no_results_link,
        "results": results
    }

    if 'items' in data:
        for item in data['items']:
            results.append({
                'title': item['title'].replace(' | UMD Libraries',''),
                'link': item['formattedUrl'],
                'description': item['snippet'],
                'item_format': 'web_page',
                'extra': {
                    'displayLink': item['displayLink'],
                    'snippet': item['snippet'],
                    'htmlSnippet': item['htmlSnippet'],
                },
            })

    return response


if __name__ == '__main__':
    # This code is not reached when running "flask run". However the Docker
    # container runs "python app.py" and host='0.0.0.0' is set to ensure
    # that flask listens on port 5000 on all interfaces.

    # Run Flask built-in server
    # app.run(host='0.0.0.0')

    # Run waitress WSGI server
    serve(TransLogger(app, setup_console_handler=True),
          host='0.0.0.0', port=5000, threads=10)
