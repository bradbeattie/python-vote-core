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

# This class implements the Schulze Proportional Ranking Method as defined
# in schulze2.pdf
from schulze_helper import SchulzeHelper
from abstract_classes import OrderingVotingSystem
from pygraph.classes.digraph import digraph

class SchulzePR(OrderingVotingSystem, SchulzeHelper):
	
	def __init__(self, ballots, tie_breaker = None, winner_threshold = None, ballot_notation = None):
		self.standardize_ballots(ballots, ballot_notation)
		super(SchulzePR, self).__init__(self.ballots,
			tie_breaker = tie_breaker,
			winner_threshold = winner_threshold,
		)
	
	def calculate_results(self):
		
		remaining_candidates = self.candidates.copy()
		self.order = []
		self.rounds = []
		
		if self.winner_threshold == None:
			winner_threshold = len(self.candidates)
		else:
			winner_threshold = min(len(self.candidates), self.winner_threshold + 1)
		
		for self.required_winners in range(1, winner_threshold):
			
			# Generate the list of patterns we need to complete
			self.generate_completed_patterns()
			self.generate_vote_management_graph()
			
			# Generate the edges between nodes
			self.graph = digraph()
			self.graph.add_nodes(remaining_candidates)
			self.winners = set([])
			self.tied_winners = set([])
			
			# Generate the edges between nodes
			for candidate_from in remaining_candidates:
				other_candidates = sorted(list(remaining_candidates - set([candidate_from])))
				for candidate_to in other_candidates:
					completed = self.proportional_completion(candidate_from, set([candidate_to]) | set(self.order))
					weight = self.strength_of_vote_management(completed)
					if weight > 0:
						self.graph.add_edge((candidate_to, candidate_from), weight)
			
			# Determine the round winner through the Schwartz set heuristic
			self.schwartz_set_heuristic()
			
			# Extract the winner and adjust the remaining candidates list
			self.order.append(self.winner)
			round = {"winner": self.winner}
			if len(self.tied_winners) > 0:
				round["tied_winners"] = self.tied_winners
			self.rounds.append(round)
			remaining_candidates -= set([self.winner])
			del self.winner
			del self.actions
			if hasattr(self, 'tied_winners'):
				del self.tied_winners
		
		# Attach the last candidate as the sole winner if necessary
		if self.winner_threshold == None or self.winner_threshold == len(self.candidates):
			self.rounds.append({"winner": list(remaining_candidates)[0]})
			self.order.append(list(remaining_candidates)[0])
		
		del self.winner_threshold
	
	def as_dict(self):
		data = super(SchulzePR, self).as_dict()
		data["rounds"] = self.rounds
		return data
