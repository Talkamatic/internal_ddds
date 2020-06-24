import logging


class FailedToGenerateMoveSequence(Exception):
    pass


class NLGenerator(object):
    def __init__(self):
        super(NLGenerator, self).__init__()
        self._logger = logging.getLogger(__name__)

    def __str__(self):
        return f"{self.__class__.__name__}"

    def generate(self, moves):
        def is_city_kpq(move):
            city_kpq = "ask(?know_answer(?X.person_city(X)))"
            return bool(move == city_kpq)

        print(moves)
        city_kpq_moves = [move for move in moves if is_city_kpq(move)]
        if len(city_kpq_moves) == 1:
            return self.generate_city_kpq_moves()
        raise FailedToGenerateMoveSequence()

    @staticmethod
    def generate_city_kpq_moves():
        utterance = "Vet du i vilken stad personen bor?"
        return utterance
