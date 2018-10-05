import flask
import requests
from jinja2 import Template
from flask import request, send_from_directory
from flask_cache import Cache
import mirador_settings
from flask_cors import CORS


def cache_key():
    return request.url


app = flask.Flask(__name__)
CORS(app)
cache = Cache(app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./"})


@app.route("/build/<path:path>")
def send_js(path):
    return send_from_directory("build", path)


@app.route("/locales/<path:path>")
def send_locale(path):
    return send_from_directory("locales", path)


@app.route("/images/<path:path>")
def send_images(path):
    return send_from_directory("images", path)


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
                if not canvas:
                    m = requests.get(manifest)
                    if m.status_code == requests.codes.ok:
                        manifest_json = m.json()
                        try:
                            canvas = manifest_json["sequences"][0]["canvases"][0]["@id"]
                            print(canvas)
                        except KeyError:
                            flask.abort(500)
                    else:
                        flask.abort(404)
            template_result = t.render(manifest_uri=manifest, canvas_uri=canvas)
            return flask.Response(template_result)
    else:
        flask.abort(500)


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000, host="0.0.0.0")
