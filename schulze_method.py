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
    def calculate_winner(ballots):
        result = CondorcetSystem.calculate_winner(ballots)
        
        # If there's a Condorcet winner, return it
        if "winners" in result:
            return result
        
        # Initialize the candidate graph
        candidate_graph = digraph()
        candidate_graph.add_nodes(list(result["candidates"]))
        for (pair,weight) in result["strong_pairs"].items():
            candidate_graph.add_edge(pair[0], pair[1], weight)
        
        # Iterate through using the Schwartz set heuristic
        candidate_graph, result["actions"] = SchulzeMethod.__schwartz_set_heuristic__(candidate_graph)
        
        # Mark the winner
        if len(candidate_graph.nodes()) == 1:
            result["winners"] = candidate_graph.nodes()[0]
        else:
            result["tied_winners"] = set(candidate_graph.nodes())
            result["tie_breaker"] = SchulzeMethod.generate_tie_breaker(result["candidates"])
            result["winners"] = set([SchulzeMethod.break_ties(candidate_graph.nodes(), result["tie_breaker"])])
        
        # Return the final result
        return result
    
    @staticmethod
    def __schwartz_set_heuristic__(candidate_graph):
        
        # Iterate through using the Schwartz set heuristic
        actions = []
        candidates = candidate_graph.nodes()
        while len(candidate_graph.edges()) > 0:
            
            # Remove nodes at the end of non-cycle paths
            access = accessibility(candidate_graph)
            mutual_access = mutual_accessibility(candidate_graph)
            candidates_to_remove = set()
            for candidate in candidates:
                candidates_to_remove = candidates_to_remove | (set(access[candidate]) - set(mutual_access[candidate]))
            if len(candidates_to_remove) > 0:
                actions.append(['nodes', candidates_to_remove])
                for candidate in candidates_to_remove:
                    candidate_graph.del_node(candidate)
                    candidates.remove(candidate)

            # If none exist, remove the weakest edges
            else:
                lightest_edges = set([candidate_graph.edges()[0]])
                weight = candidate_graph.edge_weight(candidate_graph.edges()[0][0], candidate_graph.edges()[0][1])
                for edge in candidate_graph.edges():
                    if candidate_graph.edge_weight(edge[0], edge[1]) < weight:
                        weight = candidate_graph.edge_weight(edge[0], edge[1])
                        lightest_edges = set([edge])
                    elif candidate_graph.edge_weight(edge[0], edge[1]) == weight:
                        lightest_edges.add(edge)
                actions.append(['edges', lightest_edges])
                for edge in lightest_edges:
                    candidate_graph.del_edge(edge[0], edge[1])
        
        return candidate_graph, actions
