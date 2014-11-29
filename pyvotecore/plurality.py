from __future__ import absolute_import

from .abstract_classes import AbstractSingleWinnerVotingSystem
from .plurality_at_large import PluralityAtLarge


class Plurality(AbstractSingleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None):
        super(Plurality, self).__init__(ballots, PluralityAtLarge, tie_breaker=tie_breaker)
