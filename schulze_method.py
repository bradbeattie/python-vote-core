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

from condorcet import CondorcetSystem
from pygraph.classes.digraph import digraph
from pygraph.algorithms.accessibility import accessibility, mutual_accessibility

# This class implements the Schulze Method (aka the beatpath method)
class SchulzeMethod(CondorcetSystem):
    
    def __init__(self, ballots, notation = None):
        CondorcetSystem.__init__(self, ballots, notation)
        
    def calculate_results(self):

        # Try to determine a Condorcet winner
        CondorcetSystem.calculate_results(self)
        if hasattr(self, 'winners'):
            return
        
        # Initialize the candidate graph
        self.graph = digraph()
        self.graph.add_nodes(list(self.candidates))
        for (pair,weight) in self.strong_pairs.items():
            self.graph.add_edge((pair[0], pair[1]), weight)
        
        # Iterate through using the Schwartz set heuristic
        self.schwartz_set_heuristic()
        self.graph_winner()

    def results(self):
        results = super(SchulzeMethod,self).results()
        if hasattr(self, 'actions'):
            results["actions"] = self.actions
        return results
    
    def schwartz_set_heuristic(self):
        
        # Iterate through using the Schwartz set heuristic
        self.actions = []
        while len(self.graph.edges()) > 0:
            
            # Remove nodes at the end of non-cycle paths
            access = accessibility(self.graph)
            mutual_access = mutual_accessibility(self.graph)
            candidates_to_remove = set()
            for candidate in self.graph.nodes():
                candidates_to_remove = candidates_to_remove | (set(access[candidate]) - set(mutual_access[candidate]))
            if len(candidates_to_remove) > 0:
                self.actions.append(['nodes', candidates_to_remove])
                for candidate in candidates_to_remove:
                    self.graph.del_node(candidate)

            # If none exist, remove the weakest edges
            else:
                lightest_edges = set([self.graph.edges()[0]])
                weight = self.graph.edge_weight((self.graph.edges()[0][0], self.graph.edges()[0][1]))
                for edge in self.graph.edges():
                    if self.graph.edge_weight((edge[0], edge[1])) < weight:
                        weight = self.graph.edge_weight((edge[0], edge[1]))
                        lightest_edges = set([edge])
                    elif self.graph.edge_weight((edge[0], edge[1])) == weight:
                        lightest_edges.add(edge)
                self.actions.append(['edges', lightest_edges])
                for edge in lightest_edges:
                    self.graph.del_edge((edge[0], edge[1]))