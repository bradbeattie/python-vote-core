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
    
    @staticmethod
    def calculate_winner(ballots, notation="ranking"):
        
        # Try to determine a Condorcet winner
        result = CondorcetSystem.condorcet_winner(ballots, notation)
        if "winners" in result:
            return result
        
        # Initialize the candidate graph
        graph = digraph()
        graph.add_nodes(list(result["candidates"]))
        for (pair,weight) in result["strong_pairs"].items():
            graph.add_edge(pair[0], pair[1], weight)
        
        # Iterate through using the Schwartz set heuristic
        graph, result["actions"] = SchulzeMethod.schwartz_set_heuristic(graph)
        
        # Mark the winner
        return CondorcetSystem.graph_winner(graph, result)
    
    @staticmethod
    def schwartz_set_heuristic(graph):
        
        # Remove any weak edges
        graph = CondorcetSystem.remove_weak_edges(graph)
        
        # Iterate through using the Schwartz set heuristic
        actions = []
        while len(graph.edges()) > 0:
            
            # Remove nodes at the end of non-cycle paths
            access = accessibility(graph)
            mutual_access = mutual_accessibility(graph)
            candidates_to_remove = set()
            for candidate in graph.nodes():
                candidates_to_remove = candidates_to_remove | (set(access[candidate]) - set(mutual_access[candidate]))
            if len(candidates_to_remove) > 0:
                actions.append(['nodes', candidates_to_remove])
                for candidate in candidates_to_remove:
                    graph.del_node(candidate)

            # If none exist, remove the weakest edges
            else:
                lightest_edges = set([graph.edges()[0]])
                weight = graph.edge_weight(graph.edges()[0][0], graph.edges()[0][1])
                for edge in graph.edges():
                    if graph.edge_weight(edge[0], edge[1]) < weight:
                        weight = graph.edge_weight(edge[0], edge[1])
                        lightest_edges = set([edge])
                    elif graph.edge_weight(edge[0], edge[1]) == weight:
                        lightest_edges.add(edge)
                actions.append(['edges', lightest_edges])
                for edge in lightest_edges:
                    graph.del_edge(edge[0], edge[1])
        
        return graph, actions
