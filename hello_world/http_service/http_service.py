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


@app.route("/current_time", methods=['POST'])
def current_time():
    try:
        return whq_answer_response([{"name": "10:05", "grammar_entry": None}])
    except BaseException as exception:
        return error_response(message=str(exception))

def get_value(payload, sort_name):
    if payload["request"]["parameters"][sort_name]:
        return payload["request"]["parameters"][sort_name]["value"]
    else:
        return None

@app.route("/current_alarm", methods=['POST'])
def current_alarm():
    try:
        payload = request.get_json()
        alarm_to_select = get_value(payload, "alarm_to_select")
        if alarm_to_select == "work_alarm":
            return whq_answer_response([{"grammar_entry": "The current work alarm is 9:25", "name": None}])
        if alarm_to_select == "school_alarm":
            return whq_answer_response([{"grammar_entry": "The current school alarm is 7:30", "name": None}])
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

@app.route("/SetTime", methods=['POST'])
@app.route("/SetAlarm", methods=['POST'])
@app.route("/RemoveAlarm", methods=['POST'])
@app.route("/TurnOffAlarm", methods=['POST'])
@app.route("/SelectAlarm", methods=['POST'])
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

@app.route("/Snooze", methods=['POST'])
def snooze():
    try:
        return unsuccessful_action_response("not_ringing")
    except BaseException as exception:
        return error_response(message=str(exception))

def unsuccessful_action_response(reason):
    response_template = environment.from_string(
        """
    {
      "status": "fail",
      "data": {
        "version": "1.0",
        "reason": "{{ reason }}"
      }
    }
    """
    )
    payload = response_template.render(reason=reason)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response

@app.route("/HourValidity", methods=['POST'])
def hour_validator():
    try:
        payload = request.get_json()
        value = payload["request"]["parameters"]["hour_to_set"]["value"]
        return validator_response(value < 24)
    except BaseException as exception:
        return error_response(message=exception)

@app.route("/MinuteValidity", methods=['POST'])
def minute_validator():
    try:
        payload = request.get_json()
        value = payload["request"]["parameters"]["minute_to_set"]["value"]
        return validator_response(value < 60)
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


