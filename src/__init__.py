import json
from flask import Flask, Response
from utils import repository
from utils import semver


app = Flask(__name__)


@app.route("/")
def status():
    return "Up and running"


@app.route("/<string:package_string>")
def get(package_string):
    package = semver.parse_package_string(package_string)
    try:
        package_object = repository.get(package['name'], package['version'])
        return Response(json.dumps(package_object), mimetype='application/json')
    except ValueError as e:
        return Response(json.dumps({
            'error': str(e)
        }), mimetype='application/json', status=400)
