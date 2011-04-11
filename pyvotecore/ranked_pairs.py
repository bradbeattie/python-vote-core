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

from condorcet import CondorcetSystem, CondorcetHelper
from pygraph.classes.digraph import digraph
from pygraph.algorithms.accessibility import accessibility, mutual_accessibility
from pygraph.algorithms.cycles import find_cycle
from common_functions import matching_keys
from copy import deepcopy


# This class implements the Schulze Method (aka the beatpath method)
class RankedPairs(CondorcetSystem, CondorcetHelper):
	
	def __init__(self, ballots, tie_breaker = None, ballot_notation = None):
		super(RankedPairs, self).__init__(ballots, tie_breaker = tie_breaker, ballot_notation = ballot_notation)
	
	def condorcet_completion_method(self):
		
		# Initialize the candidate graph
		self.rounds = []
		graph = digraph()
		graph.add_nodes(self.candidates)
		
		# Loop until we've considered all possible pairs
		remaining_strong_pairs = deepcopy(self.strong_pairs)
		while len(remaining_strong_pairs) > 0:
			r = {}
			
			# Find the strongest pair
			largest_strength = max(remaining_strong_pairs.values())
			strongest_pairs = matching_keys(remaining_strong_pairs, largest_strength)
			if len(strongest_pairs) > 1:
				r["tied_pairs"] = strongest_pairs
				strongest_pair = self.break_ties(strongest_pairs)
			else:
				strongest_pair = list(strongest_pairs)[0]
			r["pair"] = strongest_pair
			
			# If the pair would add a cycle, skip it
			graph.add_edge(strongest_pair)
			if len(find_cycle(graph)) > 0:
				r["action"] = "skipped"
				graph.del_edge(strongest_pair)
			else:
				r["action"] = "added"
			del remaining_strong_pairs[strongest_pair]
			self.rounds.append(r)
		
		self.old_graph = self.graph
		self.graph = graph
		self.graph_winner()
	
	def as_dict(self):
		data = super(RankedPairs, self).as_dict()
		if hasattr(self, 'rounds'):
			data["rounds"] = self.rounds
		return data
