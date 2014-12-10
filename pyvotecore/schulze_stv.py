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

# This class implements Schulze STV, a proportional representation system
from __future__ import absolute_import
import itertools

from pygraph.classes.digraph import digraph

from .abstract_classes import MultipleWinnerVotingSystem
from .schulze_helper import SchulzeHelper


class SchulzeSTV(MultipleWinnerVotingSystem, SchulzeHelper):

    def __init__(self, ballots, tie_breaker=None, required_winners=1,
                 ballot_notation=None):
        self.standardize_ballots(ballots, ballot_notation)
        super(SchulzeSTV, self).__init__(self.ballots, tie_breaker=tie_breaker,
                                         required_winners=required_winners)

    def calculate_results(self):

        # Don't bother if everyone's going to win
        super(SchulzeSTV, self).calculate_results()
        if hasattr(self, 'winners'):
            return

        # Generate the list of patterns we need to complete
        self.generate_completed_patterns()
        self.generate_vote_management_graph()

        # Build the graph of possible winners
        self.graph = digraph()
        for candidate_set in itertools.combinations(self.candidates,
                                                    self.required_winners):
            self.graph.add_nodes([tuple(sorted(list(candidate_set)))])

        # Generate the edges between nodes
        for candidate_set in itertools.combinations(self.candidates,
                                                    self.required_winners + 1):
            for candidate in candidate_set:
                other_candidates = sorted(set(candidate_set) -
                                          set([candidate]))
                completed = self.proportional_completion(candidate,
                                                         other_candidates)
                weight = self.strength_of_vote_management(completed)
                if weight > 0:
                    for subset in itertools.combinations(
                        other_candidates, len(other_candidates) - 1
                    ):
                        self.graph.add_edge((
                            tuple(other_candidates),
                            tuple(sorted(list(subset) + [candidate]))
                        ), weight)

        # Determine the winner through the Schwartz set heuristic
        self.graph_winner()

        # Split the "winner" into its candidate components
        self.winners = set(self.winner)
        del self.winner

    def as_dict(self):
        data = super(SchulzeSTV, self).as_dict()
        if hasattr(self, 'actions'):
            data['actions'] = self.actions
        return data
