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
from pygraph.algorithms.cycles import find_cycle
import copy

# This class implements Tideman's Ranked Pairs
class RankedPairs(CondorcetSystem):
    
    @staticmethod
    def calculate_winner(ballots, notation="ranking"):
        
        # Try to determine a Condorcet winner
        result = CondorcetSystem.condorcet_winner(ballots, notation)
        if "winners" in result:
            return result
        
        # Initialize the candidate graph
        result["rounds"] = []
        tie_breaker = RankedPairs.generate_tie_breaker(result["candidates"])
        graph = digraph()
        graph.add_nodes(list(result["candidates"]))
        
        # Loop until we've considered all possible pairs
        remaining_strong_pairs = copy.deepcopy(result["strong_pairs"])
        while len(remaining_strong_pairs) > 0:
            round = {}
            
            # Find the strongest pair
            largest_strength = max(remaining_strong_pairs.values())
            strongest_pairs = RankedPairs.matching_keys(remaining_strong_pairs, largest_strength)
            if len(strongest_pairs) > 1:
                result["tie_breaker"] = tie_breaker
                round["tied_pairs"] = strongest_pairs
                strongest_pair = RankedPairs.break_ties(strongest_pairs, tie_breaker)
            else:
                strongest_pair = list(strongest_pairs)[0]
            round["pair"] = strongest_pair
            
            # If the pair would add a cycle, skip it
            graph.add_edge((strongest_pair[0], strongest_pair[1]))
            if len(find_cycle(graph)) > 0:
                round["action"] = "skipped"
                graph.del_edge((strongest_pair[0], strongest_pair[1]))
            else:
                round["action"] = "added"
            del remaining_strong_pairs[strongest_pair]
            result["rounds"].append(round)
        
        # Mark the winner
        return CondorcetSystem.graph_winner(graph, result)