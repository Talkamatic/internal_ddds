from flask import Flask, request, jsonify

from src.nl_generator import NLGenerator, FailedToGenerateMoveSequence


class EnvironmentVariableNotDefinedException(Exception):
    pass


def create_app():
    flask_app = Flask(__name__)

    @flask_app.route("/generate", methods=['POST'])
    def generate():
        request_body = request.json
        moves = [move.get("semantic_expression") for move in request_body.get("moves")]
        try:
            utterance = NLGenerator().generate(moves)
            success_response = {"status": "success", "utterance": utterance}
            return jsonify(success_response)
        except FailedToGenerateMoveSequence:
            fail_response = {"status": "fail"}
            return jsonify(fail_response)
        except BaseException as exception:
            error_response = {"status": "error", "message": str(exception)}
            return jsonify(error_response)

    return flask_app
