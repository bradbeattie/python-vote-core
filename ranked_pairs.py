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

    def __init__(self, ballots, notation = None):
        CondorcetSystem.__init__(self, ballots, notation)
        
    def calculate_results(self):
        
        # Try to determine a Condorcet winner
        super(RankedPairs,self).calculate_results()
        if hasattr(self, 'winners'):
            return
        
        # Initialize the candidate graph
        self.rounds = []
        self.graph = digraph()
        self.graph.add_nodes(list(self.candidates))
        
        # Loop until we've considered all possible pairs
        remaining_strong_pairs = copy.deepcopy(self.strong_pairs)
        while len(remaining_strong_pairs) > 0:
            round = {}
            
            # Find the strongest pair
            largest_strength = max(remaining_strong_pairs.values())
            strongest_pairs = self.matching_keys(remaining_strong_pairs, largest_strength)
            if len(strongest_pairs) > 1:
                round["tied_pairs"] = strongest_pairs
                strongest_pair = self.break_ties(strongest_pairs)
            else:
                strongest_pair = list(strongest_pairs)[0]
            round["pair"] = strongest_pair
            
            # If the pair would add a cycle, skip it
            self.graph.add_edge((strongest_pair[0], strongest_pair[1]))
            if len(find_cycle(self.graph)) > 0:
                round["action"] = "skipped"
                self.graph.del_edge((strongest_pair[0], strongest_pair[1]))
            else:
                round["action"] = "added"
            del remaining_strong_pairs[strongest_pair]
            self.rounds.append(round)
        
        # Mark the winner
        self.graph_winner()
        
    def results(self):
        results = super(RankedPairs,self).results()
        if hasattr(self, 'rounds'):
            results["rounds"] = self.rounds
        return results