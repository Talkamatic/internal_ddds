import json

from flask import Flask, request
from jinja2 import Environment


app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter


def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/person", methods=['POST'])
def person():
    try:
        payload = request.get_json()
        name_dict = payload["request"]["parameters"]["person_name"]
        result = []
        name = name_dict["value"]
        if name == "arne_osvaldsson":
            result.append({"value": "person_arne_osvaldsson",
                           "sort": "person_id",
                           "grammar_entry": "Arne Osvaldsson"})
        elif name == "susanna_andersson":
            result.append({"value": "person_susanna_andersson_1",
                           "sort": "person_id",
                           "grammar_entry": "Susanna Andersson"})
            result.append({"value": "person_susanna_andersson_2",
                           "sort": "person_id",
                           "grammar_entry": "Susanna Andersson"})
        return person_response(result)
    except BaseException as exception:
        return error_response(message=str(exception))


def person_response(results):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
        {% for result in results %}
          {
            "value": {{result.value|json}},
            "confidence": 1.0,
            "grammar_entry": {{result.grammar_entry|json}}
          }{{"," if not loop.last}}
        {% endfor %}
        ]
      }
    }
     """)
    payload = response_template.render(results=results)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def _get_age(person):
    if person == "person_arne_osvaldsson":
        return 70
    elif person == "person_susanna_andersson_1":
        return 31
    elif person == "person_susanna_andersson_2":
        return 42


@app.route("/age", methods=['POST'])
def age():
    try:
        payload = request.get_json()
        person_dict = payload["request"]["parameters"]["person"]
        person = person_dict["value"]
        age = _get_age(person)
        return age_response(age)
    except BaseException as exception:
        return error_response(message=str(exception))


def age_response(age):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
          {
            "value": {{age|json}},
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """)
    payload = response_template.render(age=age)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response