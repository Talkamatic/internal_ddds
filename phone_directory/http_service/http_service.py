# coding: utf-8

import json
import traceback
import sys

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


@app.route("/person", methods=['POST'])
def person():
    try:
        payload = request.get_json()
        name_dict = payload["request"]["parameters"]["person_name"]
        name = name_dict["value"]
        city_dict = payload["request"]["parameters"]["person_city"]
        city = city_dict["value"] if city_dict else None
        age_dict = payload["request"]["parameters"]["person_age"]
        age = age_dict["value"] if age_dict else None

        landmark_dicts = payload["request"]["parameters"]["person_landmark"] or []
        landmarks = [landmark_dict["value"] for landmark_dict in landmark_dicts]
        result = []
        if name == "arne_osvaldsson":
            result.append({"value": "person_arne_osvaldsson", "sort": "person_id", "grammar_entry": "Arne Osvaldsson"})
        elif name == "susanna_andersson":
            if city in [None, "goteborg"]:
                if age in [None, 31]:
                    if not landmarks or ("slottsskogen" in landmarks and "hemkop" not in landmarks):
                        result.append({
                            "value": "person_susanna_andersson_1",
                            "sort": "person_id",
                            "grammar_entry": "Susanna Andersson"
                        })
                if age in [None, 42]:
                    if not landmarks or ("hemkop" in landmarks and "slottsskogen" not in landmarks):
                        result.append({
                            "value": "person_susanna_andersson_2",
                            "sort": "person_id",
                            "grammar_entry": "Susanna Andersson"
                        })
                if age in [None, 77]:
                    if not landmarks or "slottsskogen" in landmarks or "hemkop" in landmarks:
                        result.append({
                            "value": "person_susanna_andersson_4",
                            "sort": "person_id",
                            "grammar_entry": "Susanna Andersson"
                        })
            if city in [None, "stockholm"]:
                result.append({
                    "value": "person_susanna_andersson_3",
                    "sort": "person_id",
                    "grammar_entry": "Susanna Andersson"
                })
        elif name == "ada_kallesson":
            result.append({"value": "person_ada_kallesson_1", "sort": "person_id", "grammar_entry": "Ada Kållesson"})
            result.append({"value": "person_ada_kallesson_2", "sort": "person_id", "grammar_entry": "Ada Kållesson"})
        return person_response(result)
    except BaseException as exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_string = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(error_string)
        return error_response(message=str(exception))


def person_response(results):
    response_template = environment.from_string(
        """
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
     """
    )
    payload = response_template.render(results=results)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


def _get_age(person):
    if person == "person_arne_osvaldsson":
        return 70
    elif person == "person_susanna_andersson_1":
        return 31
    elif person == "person_susanna_andersson_2":
        return 42
    elif person == "person_ada_kallesson_2":
        return 99
    elif person == "person_susanna_andersson_4":
        return 77


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
    response_template = environment.from_string(
        """
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
     """
    )
    payload = response_template.render(age=age)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


@app.route("/phonenumber", methods=['POST'])
def phonenumber():
    try:
        payload = request.get_json()
        person_dict = payload["request"]["parameters"]["person"]
        person = person_dict["value"]
        phonenumber = _get_phonenumber(person)
        return phonenumber_response(phonenumber)
    except BaseException as exception:
        return error_response(messphonenumber=str(exception))


def phonenumber_response(phonenumber):
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
          {
            "value": {{phonenumber|json}},
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """
    )
    payload = response_template.render(phonenumber=phonenumber)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


def _get_phonenumber(person):
    if person == "person_arne_osvaldsson":
        return "070-1234570"
    elif person == "person_susanna_andersson_1":
        return "070-1234531"
    elif person == "person_susanna_andersson_2":
        return "070-1234542"
    elif person == "person_susanna_andersson_4":
        return "070-1234577"


def _get_city(person):
    if person == "person_arne_osvaldsson":
        return "goteborg"
    elif person == "person_susanna_andersson_1":
        return "goteborg"
    elif person == "person_susanna_andersson_2":
        return "goteborg"
    elif person == "person_susanna_andersson_3":
        return "stockholm"
    elif person == "person_susanna_andersson_4":
        return "goteborg"
    elif person == "person_ada_kallesson_1":
        return "goteborg"
    elif person == "person_ada_kallesson_2":
        return "goteborg"


@app.route("/city", methods=['POST'])
def city():
    try:
        payload = request.get_json()
        person_dict = payload["request"]["parameters"]["person"]
        person = person_dict["value"]
        city = _get_city(person)
        return city_response(city)
    except BaseException as exception:
        return error_response(message=str(exception))


def city_response(city):
    response_template = environment.from_string(
        """
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
          {
            "value": {{city|json}},
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """
    )
    payload = response_template.render(city=city)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response

@app.route("/action_success_response", methods=['POST'])
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
