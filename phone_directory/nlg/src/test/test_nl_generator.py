import pytest
from src.nl_generator import NLGenerator, FailedToGenerateMoveSequence


@pytest.mark.skip("unused and failing")
class TestNLGenerator(object):
    def setup(self):
        self._generator = None
        self._result = None

    def _when_generating(self, moves):
        self._moves = moves
        self._given_generator()
        self._generate_and_store_result()

    def _given_generator(self):
        self._generator = NLGenerator()

    def _generate_and_store_result(self):
        self._result = self._generator.generate(self._moves)

    def _then_result_is(self, expected):
        assert expected == self._result

    def test_generate_utterance_for_city_kpq(self):
        self._when_generating(["?know_answer(?X.person_city(X))"])
        self._then_result_is("Vet du i vilken stad personen bor?")

    def test_exception_when_failed_to_generate_move(self):
        self._given_generator()
        self._when_fail_to_generate_nl_exception_is_raised(["unexpected_move"], FailedToGenerateMoveSequence)

    def _when_fail_to_generate_nl_exception_is_raised(self, moves, expected_exception):
        with pytest.raises(expected_exception):
            self._generator.generate(moves)
