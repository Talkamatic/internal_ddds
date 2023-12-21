import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()

CITY_TYPE = {"paris": "city_type_capital", "lyon": "non_capital"}


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter


@app.route("/SomeAction", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1"
      }
    }
    """)  # yapf: disable
    payload = response_template.render()
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response
