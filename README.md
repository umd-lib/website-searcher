# website-searcher

Python 3 Flask application to search the Libraries' website; provides a backend searcher to a Bento Box style search
which expects a REST interface following the Quick Search model.

## Requires

* Python 3

## Running the Webapp

```bash
# create a .env file (then manually update environment variables)
$ cp .env-template .env
```

### Running locally

```bash
# install requirements
$ pip install -r requirements.txt

# run the app with Flask
$ flask run
```

### Running in Docker

```bash
$ docker build -t website-searcher .
$ docker run -it --rm -p 5000:5000 --env-file=.env --read-only website-searcher
```

### Endpoints

This will start the webapp listening on the default port 5000 on localhost
(127.0.0.1), and running in [Flask's debug mode].

Root endpoint (just returns `{status: ok}` to all requests):
<http://localhost:5000/>

/ping endpoint (just returns `{status: ok}` to all requests):
<http://localhost:5000/ping>

/search endpoint: <http://localhost:5000/search?q={query}>

Example:

```bash
curl 'http://localhost:5000/search?q=jstor'
{
  "endpoint": "website-search",
  "module_link": "",
  "no_results_link": "",
  "page": "1",
  "per_page": "3",
  "query": "jstor",
  "results": [
    {
      "extra": {
        "displayLink": "www.lib.umd.edu",
        "htmlSnippet": "Sep 14, 2017 <b>...</b> <b>JSTOR</b> Retention Policy | <b>JSTOR</b> is an electronic archive of core journals in the humanities, social sciences, and sciences.",
        "snippet": "Sep 14, 2017 ... JSTOR Retention Policy | JSTOR is an electronic archive of core journals in the humanities, social sciences, and sciences."
      },
      "format": "webpage",
      "link": "https://www.lib.umd.edu/collections/policies/jstor-retention-policy",
      "title": "JSTOR Retention Policy - Collections | UMD Libraries"
    },
    {
      "extra": {
        "displayLink": "www.lib.umd.edu",
        "htmlSnippet": "As the largest university library system in the Washington D.C.-Baltimore area, the University Libraries serve 37000 students and faculty of the flagship&nbsp;...",
        "snippet": "As the largest university library system in the Washington D.C.-Baltimore area, the University Libraries serve 37000 students and faculty of the flagship\u00a0..."
      },
      "format": "webpage",
      "link": "https://www.lib.umd.edu/",
      "title": "University of Maryland Libraries"
    },
    {
      "extra": {
        "displayLink": "www.lib.umd.edu",
        "htmlSnippet": "Ask Us! Directions &middot; Hours &middot; Jobs &middot; Phone Numbers &middot; Suggestions. Address: McKeldin Library, 7649 Library Lane, College Park, MD 20742-7011. Phone: (301) 405-&nbsp;...",
        "snippet": "Ask Us! Directions \u00b7 Hours \u00b7 Jobs \u00b7 Phone Numbers \u00b7 Suggestions. Address: McKeldin Library, 7649 Library Lane, College Park, MD 20742-7011. Phone: (301) 405-\u00a0..."
      },
      "format": "webpage",
      "link": "https://www.lib.umd.edu/alumniandfriends",
      "title": "Alumni and Friends | UMD Libraries"
    }
  ],
  "total": 623
}
```

[Flask's debug mode]: https://flask.palletsprojects.com/en/2.0.x/quickstart/#debug-mode

## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations.
