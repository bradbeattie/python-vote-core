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

from pygraph.algorithms.accessibility import accessibility, mutual_accessibility
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import maximum_flow
from condorcet import CondorcetHelper
from common_functions import matching_keys, unique_permutations

PREFERRED_LESS = 1
PREFERRED_SAME = 2
PREFERRED_MORE = 3
STRENGTH_TOLERANCE = 0.0000000001
STRENGTH_THRESHOLD = 0.1

# This class implements the Schulze Method (aka the beatpath method)
class SchulzeHelper(CondorcetHelper):
	
	def condorcet_completion_method(self):
		self.schwartz_set_heuristic()
	
	def schwartz_set_heuristic(self):
		
		# Iterate through using the Schwartz set heuristic
		self.actions = []
		while len(self.graph.edges()) > 0:
			access = accessibility(self.graph)
			mutual_access = mutual_accessibility(self.graph)
			candidates_to_remove = set()
			for candidate in self.graph.nodes():
				candidates_to_remove |= (set(access[candidate]) - set(mutual_access[candidate]))
			
			# Remove nodes at the end of non-cycle paths
			if len(candidates_to_remove) > 0:
				self.actions.append({'nodes': candidates_to_remove})
				for candidate in candidates_to_remove:
					self.graph.del_node(candidate)
			
			# If none exist, remove the weakest edges
			else:
				edge_weights = self.edge_weights(self.graph)
				self.actions.append({'edges': matching_keys(edge_weights, min(edge_weights.values()))})
				for edge in self.actions[-1]["edges"]:
					self.graph.del_edge(edge)
		
		self.graph_winner()
	
	def generate_vote_management_graph(self):
		self.vote_management_graph = digraph()
		self.vote_management_graph.add_nodes(self.completed_patterns)
		self.vote_management_graph.del_node(tuple([PREFERRED_MORE]*self.required_winners))
		self.pattern_nodes = self.vote_management_graph.nodes()
		self.vote_management_graph.add_nodes(["source","sink"])
		for pattern_node in self.pattern_nodes:
			self.vote_management_graph.add_edge(("source", pattern_node))
		for i in range(self.required_winners):
			self.vote_management_graph.add_node(i)
		for pattern_node in self.pattern_nodes:
			for i in range(self.required_winners):
				if pattern_node[i] == 1:
					self.vote_management_graph.add_edge((pattern_node, i))
		for i in range(self.required_winners):
			self.vote_management_graph.add_edge((i, "sink"))
	
	# Generates a list of all patterns that do not contain indifference
	def generate_completed_patterns(self):
		self.completed_patterns = []
		for i in range(0, self.required_winners + 1):
			for pattern in unique_permutations(
					[PREFERRED_LESS]*(self.required_winners-i)
					+ [PREFERRED_MORE]*(i)
			):
				self.completed_patterns.append(tuple(pattern))
	
	def proportional_completion(self, candidate, other_candidates):
		profile = dict(zip(self.completed_patterns, [0]*len(self.completed_patterns)))
		
		# Obtain an initial tally from the ballots
		for ballot in self.ballots:
			pattern = []
			for other_candidate in other_candidates:
				if ballot["ballot"][candidate] < ballot["ballot"][other_candidate]:
					pattern.append(PREFERRED_LESS)
				elif ballot["ballot"][candidate] == ballot["ballot"][other_candidate]:
					pattern.append(PREFERRED_SAME)
				else:
					pattern.append(PREFERRED_MORE)
			pattern = tuple(pattern)
			if pattern not in profile:
				profile[pattern] = 0.0
			profile[pattern] += ballot["count"]
		
		# Peel off patterns with indifference (from the most to the least) and apply proportional completion to them
		for pattern in sorted(profile.keys(), key = lambda pattern: pattern.count(PREFERRED_SAME), reverse = True):
			if pattern.count(PREFERRED_SAME) == 0: break
			self.proportional_completion_round(pattern, profile)
		
		return profile
	
	def proportional_completion_round(self, completion_pattern, profile):
		
		# Remove pattern that contains indifference
		completion_pattern_weight = profile[completion_pattern]
		del profile[completion_pattern]
		
		patterns_to_consider = {}
		for pattern in profile.keys():
			append = False
			append_target = []
			for i in range(len(completion_pattern)):
				if completion_pattern[i] == PREFERRED_SAME:
					append_target.append(pattern[i])
					if pattern[i] != PREFERRED_SAME:
						append = True
				else:
					append_target.append(completion_pattern[i])
			if append == True:
				append_target = tuple(append_target)
				if append_target not in patterns_to_consider:
					patterns_to_consider[append_target] = set()
				patterns_to_consider[append_target].add(pattern)
		
		denominator = 0
		for (append_target, patterns) in patterns_to_consider.items():
			for pattern in patterns:
				denominator += profile[pattern]
		
		# Reweight the remaining items
		for pattern in patterns_to_consider.keys():
			if denominator == 0:
				profile[pattern] += completion_pattern_weight / len(patterns_to_consider[pattern])
			else:
				if pattern not in profile:
					profile[pattern] = 0
				profile[pattern] += sum(profile[considered_pattern] for considered_pattern in patterns_to_consider[pattern]) * completion_pattern_weight / denominator
		
		return profile
	
	# This method converts the voter profile into a capacity graph and iterates
	# on the maximum flow using the Edmonds Karp algorithm. The end result is
	# the limit of the strength of the voter management as per Markus Schulze's
	# Calcul02.pdf (draft, 28 March 2008, abstract: "In this paper we illustrate
	# the calculation of the strengths of the vote managements.").
	def strength_of_vote_management(self, voter_profile):
		
		# Initialize the graph weights
		for pattern in self.pattern_nodes:
			self.vote_management_graph.set_edge_weight(("source", pattern), voter_profile[pattern])
			for i in range(self.required_winners):
				if pattern[i] == 1:
					self.vote_management_graph.set_edge_weight((pattern, i), voter_profile[pattern])
		
		# Iterate towards the limit
		r = [(float(sum(voter_profile.values())) - voter_profile[tuple([PREFERRED_MORE]*self.required_winners)]) / self.required_winners]
		while len(r) < 2 or r[-2] - r[-1] > STRENGTH_TOLERANCE:
			for i in range(self.required_winners):
				self.vote_management_graph.set_edge_weight((i, "sink"), r[-1])
			max_flow = maximum_flow(self.vote_management_graph, "source", "sink")
			sink_sum = sum(v for k,v in max_flow[0].iteritems() if k[1] == "sink")
			r.append(sink_sum/self.required_winners)
			
			# We expect strengths to be above a specified threshold
			if sink_sum < STRENGTH_THRESHOLD:
				return 0
		
		# Return the final max flow
		return round(r[-1],9)
