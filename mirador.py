import flask
import requests
from jinja2 import Template
from datetime import timedelta
from flask import make_response, request, current_app, send_from_directory
from functools import update_wrapper
from flask_cache import Cache
import mirador_settings

print('Cache timeout', mirador_settings.cache_timeout)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


def cache_key():
    return request.url


app = flask.Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': './'})

@app.route('/build/<path:path>')
def send_js(path):
    return send_from_directory('build', path)


@app.route('/mirador', methods=['GET'])
@crossdomain(origin='*')
@cache.cached(timeout=int(mirador_settings.cache_timeout), key_prefix=cache_key)
def mirador():
    """
    Flask app.

    Expects an md5 hashed annotation container  as part of the path.

    Montague stores annotations in a container based on the md5 hash of
    the canvas uri.

    Requests the annotation list from Elucidate, using the IIIF context.

    Unpacks the annotation list, and reformats the JSON to be in the
    IIIF Presentation API annotation list format.

    Returns JSON-LD for an annotation list.

    The @id of the annotation list is set to the request_url.
    """
    with open('index.html', 'r') as local_template:
        mirador_template = local_template.read()
    if mirador_template:
        t = Template(mirador_template)
        if flask.request.method == 'GET':
            manifest = request.args.get('manifest', default=None, type=str)
            canvas = request.args.get('canvas', default=None, type=str)
            if manifest:
                if not canvas:
                    m = requests.get(manifest)
                    if m.status_code == requests.codes.ok:
                        manifest_json = m.json()
                        try:
                            canvas = manifest_json['sequences'][0]['canvases'][0]['@id']
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
    app.run(threaded=True, debug=True, port=5000, host='0.0.0.0')
