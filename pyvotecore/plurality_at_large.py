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
from pyvotecore.common_functions import matching_keys
import types
import copy


class PluralityAtLarge(MultipleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None, required_winners=1):
        super(PluralityAtLarge, self).__init__(ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):

        # Standardize the ballot format and extract the candidates
        self.candidates = set()
        for ballot in self.ballots:

            # Convert single candidate ballots into ballot lists
            if not isinstance(ballot["ballot"], types.ListType):
                ballot["ballot"] = [ballot["ballot"]]

            # Ensure no ballot has an excess of votes
            if len(ballot["ballot"]) > self.required_winners:
                raise Exception("A ballot contained too many candidates")

            # Add all candidates on the ballot to the set
            self.candidates.update(set(ballot["ballot"]))

        # Sum up all votes for each candidate
        self.tallies = dict.fromkeys(self.candidates, 0)
        for ballot in self.ballots:
            for candidate in ballot["ballot"]:
                self.tallies[candidate] += ballot["count"]
        tallies = copy.deepcopy(self.tallies)

        # Determine which candidates win
        winning_candidates = set()
        while len(winning_candidates) < self.required_winners:

            # Find the remaining candidates with the most votes
            largest_tally = max(tallies.values())
            top_candidates = matching_keys(tallies, largest_tally)

            # Reduce the found candidates if there are too many
            if len(top_candidates | winning_candidates) > self.required_winners:
                self.tied_winners = top_candidates.copy()
                while len(top_candidates | winning_candidates) > self.required_winners:
                    top_candidates.remove(self.break_ties(top_candidates, True))

            # Move the top candidates into the winning pile
            winning_candidates |= top_candidates
            for candidate in top_candidates:
                del tallies[candidate]

        self.winners = winning_candidates

    def as_dict(self):
        data = super(PluralityAtLarge, self).as_dict()
        data["tallies"] = self.tallies
        return data
