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
class SchulzeMethod(CondorcetSystem):
    
    @staticmethod
    def calculateWinner(ballots):
        result = CondorcetSystem.calculateWinner(ballots)
        
        # If there's a Condorcet winner, return it
        if "winners" in result:
            return result
        
        # Initialize the candidate graph
        candidateGraph = digraph()
        candidateGraph.add_nodes(list(result["candidates"]))
        for (pair,weight) in result["strongPairs"].items():
            candidateGraph.add_edge(pair[0], pair[1], weight)
        
        # Iterate through using the Schwartz set heuristic
        result["actions"] = []
        candidates = result["candidates"].copy()
        while len(candidateGraph.edges()) > 0:
            
            # Remove nodes at the end of non-cycle paths
            access = accessibility(candidateGraph)
            mutualAccess = mutual_accessibility(candidateGraph)
            candidatesToRemove = set()
            for candidate in candidates:
                candidatesToRemove = candidatesToRemove | (set(access[candidate]) - set(mutualAccess[candidate]))
            if len(candidatesToRemove) > 0:
                result["actions"].append(['nodes', candidatesToRemove])
                for candidate in candidatesToRemove:
                    candidateGraph.del_node(candidate)
                    candidates.remove(candidate)

            # If none exist, remove the weakest edges
            else:
                lightestEdges = set([candidateGraph.edges()[0]])
                weight = candidateGraph.edge_weight(candidateGraph.edges()[0][0], candidateGraph.edges()[0][1])
                for edge in candidateGraph.edges():
                    if candidateGraph.edge_weight(edge[0], edge[1]) < weight:
                        weight = candidateGraph.edge_weight(edge[0], edge[1])
                        lightestEdges = set([edge])
                    elif candidateGraph.edge_weight(edge[0], edge[1]) == weight:
                        lightestEdges.add(edge)
                result["actions"].append(['edges', lightestEdges])
                for edge in lightestEdges:
                    candidateGraph.del_edge(edge[0], edge[1])
        
        # Mark the winner
        if len(candidateGraph.nodes()) == 1:
            result["winners"] = candidateGraph.nodes()[0]
        else:
            result["tiedWinners"] = set(candidateGraph.nodes())
            result["tieBreaker"] = SchulzeMethod.generateTieBreaker(result["candidates"])
            result["winners"] = set([SchulzeMethod.breakWinnerTie(candidateGraph.nodes(), result["tieBreaker"])])
        
        # Return the final result
        return result