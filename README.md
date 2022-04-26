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

/search endpoint: `http://localhost:5000/search?q={query}&page={page number?}&per_page={results per page?}`

Example:

```bash
curl 'http://localhost:5000/search?q=jstor&per_page=3&page=0'
{
  "endpoint": "website-search",
  "module_link": "https://search.lib.umd.edu/website?query=jstor",
  "no_results_link": "https://search.lib.umd.edu/website",
  "page": "0",
  "per_page": "3",
  "query": "jstor",
  "results": [
    {
      "description": "Sep 14, 2017 ... JSTOR Retention Policy | JSTOR is an electronic archive of core journals in the humanities, social sciences, and sciences.",
      "extra": {
        "displayLink": "www.lib.umd.edu",
        "htmlSnippet": "Sep 14, 2017 <b>...</b> <b>JSTOR</b> Retention Policy | <b>JSTOR</b> is an electronic archive of core journals in the humanities, social sciences, and sciences.",
        "snippet": "Sep 14, 2017 ... JSTOR Retention Policy | JSTOR is an electronic archive of core journals in the humanities, social sciences, and sciences."
      },
      "item_format": "web_page",
      "link": "https://www.lib.umd.edu/collections/policies/jstor-retention-policy",
      "title": "JSTOR Retention Policy - Collections"
    },
    {
      "description": "As the largest university library system in the Washington D.C.-Baltimore area, the University Libraries serve 37000 students and faculty of the flagship ...",
      "extra": {
        "displayLink": "www.lib.umd.edu",
        "htmlSnippet": "As the largest university library system in the Washington D.C.-Baltimore area, the University Libraries serve 37000 students and faculty of the flagship&nbsp;...",
        "snippet": "As the largest university library system in the Washington D.C.-Baltimore area, the University Libraries serve 37000 students and faculty of the flagship ..."
      },
      "item_format": "web_page",
      "link": "https://www.lib.umd.edu/",
      "title": "University of Maryland Libraries"
    },
    {
      "description": "Oct 7, 2021 ... Remote access to library resources is available for all current University of Maryland, College Park students, faculty, and staff. Database ...",
      "extra": {
        "displayLink": "www.lib.umd.edu",
        "htmlSnippet": "Oct 7, 2021 <b>...</b> Remote access to library resources is available for all current University of Maryland, College Park students, faculty, and staff. Database&nbsp;...",
        "snippet": "Oct 7, 2021 ... Remote access to library resources is available for all current University of Maryland, College Park students, faculty, and staff. Database ..."
      },
      "item_format": "web_page",
      "link": "https://www.lib.umd.edu/services/remote-access",
      "title": "How do I Connect to Electronic Resources Off-Campus? | UMD ..."
    }
  ],
  "total": 854
}

```

[Flask's debug mode]: https://flask.palletsprojects.com/en/2.0.x/quickstart/#debug-mode

## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations.
