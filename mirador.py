import flask
import requests
from jinja2 import Template
from flask import request, send_from_directory
from flask_caching import Cache
import mirador_settings
from flask_cors import CORS
import sys
import logging


def cache_key():
    return request.url


app = flask.Flask(__name__, static_folder="build")
CORS(app)
cache = Cache(app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./cache/"})


@app.route("/<path:filename>")
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/mirador", methods=["GET"])
@cache.cached(timeout=int(mirador_settings.cache_timeout), key_prefix=cache_key)
def mirador():
    """
    Flask app.

    Renders a simple Jinja template with Mirador populated with the right manifest and canvas URIs.
    
    """
    with open("index.html", "r") as local_template:
        mirador_template = local_template.read()
    if mirador_template:
        t = Template(mirador_template)
        if flask.request.method == "GET":
            manifest = request.args.get("manifest", default=None, type=str)
            canvas = request.args.get("canvas", default=None, type=str)
            if manifest:
                manifest_json = None
                m = requests.get(manifest)
                if m.status_code == requests.codes.ok:
                    manifest_json = m.json()
                else:
                    logging.error("The manifest request returned %s", m.status_code)
                    flask.abort(m.status_code)
                if not canvas:
                    if manifest_json:
                        try:
                            logging.debug("Using first canvas by default.")
                            canvas = manifest_json["sequences"][0]["canvases"][0]["@id"]
                        except KeyError:
                            logging.error("Could not identify first canvas in manifest")
                            flask.abort(500)
                    else:
                        logging.error("No manifest available.")
                        flask.abort(404)
            template_result = t.render(manifest_uri=manifest, canvas_uri=canvas)
            return flask.Response(template_result)
        else:
            logging.error("Unsupported HTTP method.")
            flask.abort(405)
    else:
        logging.error("Could not find JINJA2 template.")
        flask.abort(500)


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    )
    app.run(threaded=True, debug=True, port=5000, host="0.0.0.0")
