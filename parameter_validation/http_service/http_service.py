import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter


def error_response(message):
    response_template = environment.from_string(
        """
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """
    )
    payload = response_template.render(message=message)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


@app.route("/validate", methods=['POST'])
def flavour_validator():
    try:
        return validator_response(is_valid=True)
    except BaseException as exception:
        return error_response(message=exception)


def validator_response(is_valid):
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """
    )
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response
