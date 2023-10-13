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


JOHN = "first_name_john"
ANNA = "first_name_anna"

JOHNSON = "last_name_johnson"
THOMPSON = "last_name_thompson"

JOHN_JOHNSON = "contact_john_johnson"
JOHN_THOMPSON = "contact_john_thompson"
ANNA_JOHNSON = "contact_anna_johnson"
ANNA_THOMPSON = "contact_anna_thompson"

CONTACTS = {
    JOHN_JOHNSON: {
        "first_name": JOHN,
        "last_name": JOHNSON,
    },
    JOHN_THOMPSON: {
        "first_name": JOHN,
        "last_name": THOMPSON,
    },
    ANNA_JOHNSON: {
        "first_name": ANNA,
        "last_name": JOHNSON
    },
}

FIRST_NAMES = {"John": JOHN, "Anna": ANNA}

LAST_NAMES = {
    "Johnson": JOHNSON,
    "Thompson": THOMPSON,
}


def contacts_with_matching_first_name(name):
    if name:
        return {contact_id for contact_id in CONTACTS if CONTACTS[contact_id]["first_name"] == name}
    else:
        return {contact_id for contact_id in CONTACTS}

def contacts_with_matching_last_name(name):
    if name:
        return {contact_id for contact_id in CONTACTS if CONTACTS[contact_id]["last_name"] == name}
    else:
        return {contact_id for contact_id in CONTACTS}

def get_value(payload, sort_name):
    if payload["request"]["parameters"][sort_name]:
        return payload["request"]["parameters"][sort_name]["value"]
    else:
        return None

def full_name_of(contact_id):
    contact = CONTACTS[contact_id]
    for name in FIRST_NAMES:
        if contact["first_name"] == FIRST_NAMES[name]:
            first_name = name
    for name in LAST_NAMES:
        if contact["last_name"] == LAST_NAMES[name]:
            last_name = name
    return f"{first_name} {last_name}"

def get_grammar_entry(payload, sort_name):
    return payload["request"]["parameters"][sort_name]["grammar_entry"]


@app.route("/selected_contact", methods=['POST'])
def selected_contact():
    def available_contacts(first_name, last_name):
        matching_first_name_contacts = contacts_with_matching_first_name(first_name)
        matching_last_name_contacts = contacts_with_matching_last_name(last_name)
        available_contacts = matching_first_name_contacts.intersection(matching_last_name_contacts)
        return available_contacts
    
    try:
        payload = request.get_json()
        first_name = get_value(payload, "selected_first_name")
        last_name = get_value(payload, "selected_last_name")
        contacts = available_contacts(first_name, last_name)
        result = []
        for contact_id in contacts:
            full_name = full_name_of(contact_id)
            result.append({"name": contact_id, "sort": "contact", "grammar_entry": full_name})
        return whq_answer_response(result)
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


@app.route("/DeleteNumber", methods=['POST'])
@app.route("/Call", methods=['POST'])
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
