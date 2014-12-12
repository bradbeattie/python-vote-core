from __future__ import absolute_import

from .abstract_classes import AbstractSingleWinnerVotingSystem
from .stv import STV


class IRV(AbstractSingleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None):
        super(IRV, self).__init__(ballots, STV, tie_breaker=tie_breaker)

    def calculate_results(self):
        super(IRV, self).calculate_results()
        IRV.singularize(self.rounds)

    def as_dict(self):
        data = super(IRV, self).as_dict()
        IRV.singularize(data["rounds"])
        return data

    @staticmethod
    def singularize(rounds):
        for r in rounds:
            if "winners" in r:
                r["winner"] = list(r["winners"])[0]
                del r["winners"]
