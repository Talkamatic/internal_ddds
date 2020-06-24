from flask import url_for


class TestServe(object):
    def setup(self):
        self._client = None

    def test_successful_response_for_city_kpq(self, client):
        self._given_client(client)
        self._when_receiving_request(
            '{"moves": [{"semantic_expression": "?know_answer(?X.person_city(X))"}]}'
        )
        self._then_response_is({
            "status": "success",
            "utterance": "Vet du i vilken stad personen bor?"
        })

    def test_fail_status_response(self, client):
        self._given_client(client)
        self._when_receiving_request('{"moves": [{"semantic_expression": "unexpected_move"}]}')
        self._then_response_is({"status": "fail"})

    def _given_client(self, client):
        self._client = client

    def _when_receiving_request(self, request_data):
        self._response = self._client.post(
            url_for("generate"), data=request_data, headers={'Content-type': 'application/json'}
        )

    def _then_response_is(self, expected_data):
        assert self._response.get_json() == expected_data
