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

from voting_system import VotingSystem
from pygraph.classes.digraph import digraph
import itertools

# This class determines the Condorcet winner if one exists.
class CondorcetSystem(VotingSystem):
    
    def __init__(self, ballots, notation = "rating"):
        self.candidates, self.ballots = self.convert_ballots(ballots, notation)
        VotingSystem.__init__(self)
    
    def calculate_results(self):
        self.graph = self.ballots_into_graph(self.candidates, self.ballots)
        self.pairs = CondorcetSystem.edge_weights(self.graph)
        self.remove_weak_edges(self.graph)
        self.strong_pairs = CondorcetSystem.edge_weights(self.graph)
        self.graph_winner()

    def results(self):
        results = VotingSystem.results(self)
        if hasattr(self, 'pairs'):
            results["pairs"] = self.pairs
        if hasattr(self, 'strong_pairs'):
            results["strong_pairs"] = self.strong_pairs
        if hasattr(self, 'tied_winners'):
            results["tied_winners"] = self.tied_winners
        return results
    
    def graph_winner(self):
        losing_candidates = set([edge[1] for edge in self.graph.edges()])
        winning_candidates = set(self.graph.nodes()) - losing_candidates
        if len(winning_candidates) == 1:
            self.winners = set([list(winning_candidates)[0]])
        elif len(winning_candidates) > 1:
            self.tied_winners = set(self.graph.nodes())
            self.winners = set([self.break_ties(winning_candidates)])

    @staticmethod
    def ballots_into_graph(candidates, ballots):
        graph = digraph()
        graph.add_nodes(candidates)
        for pair in itertools.permutations(candidates, 2):
            graph.add_edge(pair, sum([
                ballot["count"]
                for ballot in ballots
                if ballot["ballot"][pair[0]] > ballot["ballot"][pair[1]]
            ]))
        return graph
    
    @staticmethod
    def edge_weights(graph):
        return dict([
            (edge, graph.edge_weight(edge))
            for edge in graph.edges()
        ])
    
    @staticmethod
    def remove_weak_edges(graph):
        for pair in itertools.combinations(graph.nodes(), 2):
            pairs = (pair, (pair[1], pair[0]))
            weights = (graph.edge_weight(pairs[0]), graph.edge_weight(pairs[1]))
            if weights[0] >= weights[1]:
                graph.del_edge(pairs[1])
            if weights[1] >= weights[0]:
                graph.del_edge(pairs[0])
    
    @staticmethod
    def convert_ballots(ballots, notation):
        
        if notation == "grouping":
            for ballot in ballots:
                ballot["ballot"].reverse()
                new_ballot = {}
                r = 0
                for rank in ballot["ballot"]:
                    r += 1
                    for candidate in rank:
                        new_ballot[candidate] = r
                ballot["ballot"] = new_ballot
        
        elif notation == "ranking":
            for ballot in ballots:
                for candidate, rating in ballot["ballot"].iteritems():
                    ballot["ballot"][candidate] = -float(rating)

        elif notation == "rating":
            for ballot in ballots:
                for candidate, rating in ballot["ballot"].iteritems():
                    ballot["ballot"][candidate] = float(rating)
        
        else:
            raise Exception("Unknown notation specified")
        
        candidates = set()
        for ballot in ballots:
            candidates |= set(ballot["ballot"].keys())
        
        for ballot in ballots:
            lowest_preference = min(ballot["ballot"].values()) - 1
            for candidate in candidates - set(ballot["ballot"].keys()):
                ballot["ballot"][candidate] = lowest_preference
        
        return candidates, ballots