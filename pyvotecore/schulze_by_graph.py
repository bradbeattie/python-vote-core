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

from schulze_method import SchulzeMethod
from schulze_helper import SchulzeHelper
from abstract_classes import AbstractOrderingVotingSystem
from pygraph.classes.digraph import digraph


# This class provides Schulze Method results, but bypasses ballots and uses preference tallies instead. 
class SchulzeMethodByGraph(SchulzeMethod):
	
	def __init__(self, edges, tie_breaker = None, ballot_notation = None):
		self.edges = edges
		super(SchulzeMethodByGraph, self).__init__([], tie_breaker = tie_breaker, ballot_notation = ballot_notation)
	
	def standardize_ballots(self, ballots, ballot_notation):
		self.ballots = []
		self.candidates = set([edge[0] for edge, weight in self.edges.iteritems()]) | set([edge[1] for edge, weight in self.edges.iteritems()])
	
	def ballots_into_graph(self, candidates, ballots):
		graph = digraph()
		graph.add_nodes(candidates)
		for edge in self.edges.iteritems():
			graph.add_edge(edge[0], edge[1])
		return graph

# This class provides Schulze NPR results, but bypasses ballots and uses preference tallies instead.
class SchulzeNPRByGraph(AbstractOrderingVotingSystem, SchulzeHelper):
	
	def __init__(self, edges, winner_threshold = None, tie_breaker = None, ballot_notation = None):
		self.edges = edges
		self.candidates = set([edge[0] for edge, weight in edges.iteritems()]) | set([edge[1] for edge, weight in edges.iteritems()])
		super(SchulzeNPRByGraph, self).__init__([],
			single_winner_class = SchulzeMethodByGraph,
			winner_threshold = winner_threshold,
			tie_breaker = tie_breaker,
		)
	
	def ballots_without_candidate(self, ballots, candidate):
		self.edges = dict([(edge, weight) for edge, weight in self.edges.iteritems() if edge[0] != candidate and edge[1] != candidate])
		return self.edges
	
	def calculate_results(self):
		self.ballots = self.edges
		super(SchulzeNPRByGraph, self).calculate_results()