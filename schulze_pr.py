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
from schulze_stv import SchulzeSTV
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import maximum_flow
import itertools

class SchulzePR(SchulzeSTV):
    
    def __init__(self, ballots, notation = None):
        SchulzeSTV.__init__(self, ballots, 1, notation)
        
    def results(self):
        results = {
            "candidates": self.candidates,
            "winners": self.winners
        }
        if hasattr(self, 'actions'):
            results["actions"] = self.actions
        if hasattr(self, 'tied_winners'):
            results["tied_winners"] = self.tied_winners
            results["tie_breaker"] = self.tie_breaker
        return results
        
    def calculate_results(self):
        
        self.required_winners = 1
        
        remaining_candidates = self.candidates
        self.order = []
        
        print "BALLOTS"
        for ballot in self.ballots:
            print ballot
        print
        
        #while len(remaining_candidates) > 1:
        print "REMAINING CANDIDATES", remaining_candidates
        print
        
        self.__generate_completion_patterns__()
        self.__generate_completed_patterns__()
        print "COMPLETION PATTERNS",self.completion_patterns
        print "COMPLETED PATTERNS",self.completed_patterns
        
        # Prepare the vote management graph
        self.vote_management_graph = digraph()
        self.vote_management_graph.add_nodes(self.completed_patterns)
        self.vote_management_graph.del_node(tuple([3]*self.required_winners))
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
        
        # Generate the edges between nodes
        for candidate_from in remaining_candidates:
            other_candidates = sorted(list(remaining_candidates - set([candidate_from])))
            for candidate_to in other_candidates:
                print "FROM %s TO %s" % (candidate_from, candidate_to)
                completed = self.__proportional_completion__(candidate_from, candidate_to)
                print "COMPLETED", completed
                
                weight = self.__strength_of_vote_management__(completed)
                print "WEIGHT", weight
                #if weight > 0:
                #    for subset in itertools.combinations(other_candidates, len(other_candidates) - 1):
                #        self.graph.add_edge((tuple(other_candidates), tuple(sorted(list(subset) + [candidate]))), weight)
                
                print
                candidate_from = "b"
                candidate_to = "a"
                print "FROM %s TO %s" % (candidate_from, candidate_to)
                completed = self.__proportional_completion__(candidate_from, candidate_to)
                print "COMPLETED", completed
                
                weight = self.__strength_of_vote_management__(completed)
                print "WEIGHT", weight
                #if weight > 0:
                #    for subset in itertools.combinations(other_candidates, len(other_candidates) - 1):
                #        self.graph.add_edge((tuple(other_candidates), tuple(sorted(list(subset) + [candidate]))), weight)

                
                return
            print

    def __generate_completion_patterns__(self):
        self.completion_patterns = []
        for i in range(0,self.required_winners):
            for j in range(0, i+1):
                for pattern in self.__unique_permutations__([2]*(self.required_winners-i)+[1]*(j)+[3]*(i-j)):
                    self.completion_patterns.append(tuple(pattern))
        
    def __generate_completed_patterns__(self):
        self.completed_patterns = []
        for i in range(0,self.required_winners + 1):
            for pattern in self.__unique_permutations__([1]*(self.required_winners-i)+[3]*(i)):
                self.completed_patterns.append(tuple(pattern))
    