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


@app.route("/url_to_play", methods=['POST'])
def url_to_play():
    try:
        return whq_answer_response([{"name": "mock_audio_url", "grammar_entry": None}])
    except BaseException as exception:
        return error_response(message=str(exception))

def whq_answer_response(individuals):
    response_template = environment.from_string(
        """
        {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
        {% for individual in individuals %}
          {
            "value": {{ individual["name"]|json }},
            "confidence": 1.0,
            "grammar_entry": "{{ individual["grammar_entry"]  }}"
          } {{ "" if loop.last else ", " }}
        {% endfor %}
        ]
      }
    }
    """
    )
    payload = response_template.render(individuals=individuals)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


@app.route("/MockAction", methods=['POST'])
@app.route("/SetVolume", methods=['POST'])
@app.route("/SetDepartureDay", methods=['POST'])
@app.route("/NavigateToDestination", methods=['POST'])
@app.route("/MockAction", methods=['POST'])
def successful_action():
    try:
        return successful_action_response()
    except BaseException as exception:
        return error_response(message=str(exception))


def successful_action_response():
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.0"
      }
    }
    """
    )
    payload = response_template.render()
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response
