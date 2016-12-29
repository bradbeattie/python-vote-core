# Copyright (C) 2009, Brad Beattie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyvotecore.abstract_classes import MultipleWinnerVotingSystem
from collections import defaultdict
from pyvotecore.common_functions import matching_keys
import copy
import math


# This class implements the Single Transferable vote (aka STV) in its most
# classic form (see http://en.wikipedia.org/wiki/Single_transferable_vote).
# Alternate counting methods such as Meek's and Warren's would be nice, but
# would need to be covered in a separate class.
class STV(MultipleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None, required_winners=1):
        super(STV, self).__init__(ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):

        self.candidates = set()
        for ballot in self.ballots:
            ballot["count"] = float(ballot["count"])
            self.candidates.update(ballot["ballot"])
        if len(self.candidates) < self.required_winners:
            raise Exception("Not enough candidates provided")

        self.quota = STV.droop_quota(self.ballots, self.required_winners)
        self.rounds = []
        self.winners = set()
        quota = self.quota
        ballots = copy.deepcopy(self.ballots)
        remaining_candidates = self.candidates - self.winners

        # Loop until we have enough candidates
        while len(self.winners) < self.required_winners and len(remaining_candidates) + len(self.winners) != self.required_winners:

            # Repopulate the remaining candidates if necessary
            if not remaining_candidates:
                remaining_candidates = self.candidates - self.winners

            # If all the votes have been used up, start from scratch for the remaining candidates
            round = {}
            if len(list(filter(lambda ballot: ballot["count"] > 0 and ballot["ballot"], ballots))) == 0:
                remaining_candidates = self.candidates - self.winners
                round["note"] = "reset"
                ballots = copy.deepcopy(self.ballots)
                for ballot in ballots:
                    ballot["ballot"] = filter(lambda x: x in remaining_candidates, ballot["ballot"])
                quota = STV.droop_quota(ballots, self.required_winners - len(self.winners))

            round["tallies"] = self.tallies(ballots)
            if round["tallies"]:

                # If any candidates meet or exceeds the quota, they're a winner
                if max(round["tallies"].values()) >= quota:

                    # Collect candidates as winners
                    round["winners"] = set([
                        candidate
                        for candidate, tally in round["tallies"].items()
                        if tally >= self.quota
                    ])
                    self.winners |= round["winners"]
                    remaining_candidates -= round["winners"]

                    # Redistribute excess votes
                    for ballot in ballots:
                        if ballot["ballot"] and ballot["ballot"][0] in round["winners"]:
                            ballot["count"] *= (round["tallies"][ballot["ballot"][0]] - self.quota) / round["tallies"][ballot["ballot"][0]]

                    # Remove candidates from remaining ballots
                    ballots = self.remove_candidates_from_ballots(round["winners"], ballots)

                # If no candidate exceeds the quota, elimiate the least preferred
                else:
                    round.update(self.loser(round["tallies"]))
                    remaining_candidates.remove(round["loser"])
                    ballots = self.remove_candidates_from_ballots([round["loser"]], ballots)

            # Record this round's actions
            self.rounds.append(round)

        # Append the final winner and return
        if len(self.winners) < self.required_winners:
            self.remaining_candidates = remaining_candidates
            self.winners |= self.remaining_candidates

    def as_dict(self):
        data = super(STV, self).as_dict()
        data["quota"] = self.quota
        data["rounds"] = self.rounds
        if hasattr(self, 'remaining_candidates'):
            data["remaining_candidates"] = self.remaining_candidates
        return data

    def loser(self, tallies):
        losers = matching_keys(tallies, min(tallies.values()))
        if len(losers) == 1:
            return {"loser": list(losers)[0]}
        else:
            return {
                "tied_losers": losers,
                "loser": self.break_ties(losers, True)
            }

    @staticmethod
    def remove_candidates_from_ballots(candidates, ballots):
        for ballot in ballots:
            for candidate in candidates:
                if candidate in ballot["ballot"]:
                    ballot["ballot"].remove(candidate)
        return ballots

    def tallies(self, ballots):
        tallies = dict()
        for ballot in ballots:
            for candidate in ballot["ballot"]:
                tallies[candidate] = 0
        for ballot in ballots:
            if ballot["ballot"]:
                tallies[ballot["ballot"][0]] += ballot["count"]
        return dict((candidate, votes) for (candidate, votes) in tallies.items())

    @staticmethod
    def droop_quota(ballots, seats=1):
        voters = 0
        for ballot in ballots:
            if ballot["ballot"]:
                voters += ballot["count"]
        return int(math.floor(voters / (seats + 1)) + 1)
