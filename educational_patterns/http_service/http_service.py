# -*- coding: utf-8 -*-

import json
from os import getenv
import os

from flask import Flask, request
from jinja2 import Environment
from elasticapm.contrib.flask import ElasticAPM


app = Flask(__name__)
apm = ElasticAPM()
apm.init_app(app, service_name=getenv('APM_SERVICE_NAME', default=""), server_url=getenv('APM_SERVER_URL', default=""))
environment = Environment()

EXPLANATIONS = {
    "nordbor": "personer som bor i de nordiska länderna",
    "vikingatiden": "en period i historien då vikingarna levde",
    "handelsmän": "personer som åker runt och handlar med andra folk",
    "aggressiva": "beteende eller reaktion som har till syfte att skada en annan person",
    "strider": "strider kan utkämpas i ett krig då man slåss mot varandra",
}

def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter


def store_stats(session_id, data, current_question, key, value):
    file_name = f'stats-{session_id}.json'
    file = open(file_name, 'w')
    if isinstance(data, dict):
        if key in data:
            data[key][0] = data[key][0] + value
            data[key][1].append(current_question)
        else:
            data[key] = [value, [current_question]]
    json.dump(data, file)
    file.close()


def retrieve_stats(session_id):
    file_name = f'stats-{session_id}.json'
    if not os.path.exists(file_name):
        data = {}
        with open(file_name, 'w') as file:
            json.dump(data, file)
    with open(file_name, 'r') as file:
        filedata = file.read()
    data = json.loads(filedata)
    return data


def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)  # yapf: disable
    payload = response_template.render(message=message)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """)  # yapf: disable
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


def multiple_query_response(results):
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
    """)  # yapf: disable
    payload = response_template.render(results=results)
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
    """)  # yapf: disable
    payload = response_template.render()
    response = app.response_class(response=payload, status=200, mimetype='application/json')
    return response


def validity_response(status):
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1",
       "is_valid": {{status|json}}
     }
   }
   """)
    payload = response_template.render(status=status)
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
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


@app.route("/explanation_of_word", methods=['POST'])
def explanation_of_word():
    try:
        payload = request.get_json()
        word_to_explain = payload["request"]["parameters"]["word_to_explain"]["value"]
        explanation = EXPLANATIONS.get(word_to_explain)
        if explanation is None:
            return query_response(value=f"Det vet jag inte vad det betyder.", grammar_entry=None)
        return query_response(value=explanation, grammar_entry=None)
    except BaseException as exception:
        return error_response(message=str(exception))


@app.route("/rw_vad_kallade_de_landet_darx_validity", methods=['POST'])
def rw_vad_kallade_de_landet_darx_validity():
    payload = request.get_json()
    rw_vad_kallade_de_landet_darx = payload["request"]["parameters"]["rw_vad_kallade_de_landet_darx"]["value"]
    if rw_vad_kallade_de_landet_darx == "rw_vad_kallade_de_landet_darx_correct":
        return validity_response(True)
    return validity_response(False)
