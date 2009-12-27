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
    def calculateWinner(ballots):
        result = CondorcetSystem.calculateWinner(ballots)
        
        # If there's a Condorcet winner, return it
        if "winners" in result:
            return result
        
        # Initialize the candidate graph
        result["rounds"] = []
        tieBreaker = RankedPairs.generateTieBreaker(result["candidates"])
        candidateGraph = digraph()
        candidateGraph.add_nodes(list(result["candidates"]))
        
        # Loop until we've considered all possible pairs
        remainingStrongPairs = copy.deepcopy(result["strongPairs"])
        while len(remainingStrongPairs) > 0:
            round = {}
            
            # Find the strongest pair
            largestStrength = max(remainingStrongPairs.values())
            strongestPairs = RankedPairs.matchingKeys(remainingStrongPairs, largestStrength)
            if len(strongestPairs) > 1:
                result["tieBreaker"] = tieBreaker
                round["tiedPairs"] = strongestPairs
                strongestPair = RankedPairs.breakStrongestPairTie(strongestPairs, tieBreaker)
            else:
                strongestPair = list(strongestPairs)[0]
            round["pair"] = strongestPair
            
            # If the pair would add a cycle, skip it
            candidateGraph.add_edge(strongestPair[0], strongestPair[1])
            if len(find_cycle(candidateGraph)) > 0:
                round["action"] = "skipped"
                candidateGraph.del_edge(strongestPair[0], strongestPair[1])
            else:
                round["action"] = "added"
            del remainingStrongPairs[strongestPair]
            result["rounds"].append(round)
        
        # The winner is any candidate with no losses (if there are 2+, use the tiebreaker)
        winners = result["candidates"].copy()
        for edge in candidateGraph.edges():
            if edge[1] in winners:
                winners.remove(edge[1])
        
        # Mark the winner
        if len(winners) == 1:
            result["winners"] = set([list(winners)[0]])
        else:
            result["tiedWinners"] = winners
            result["tieBreaker"] = tieBreaker
            result["winners"] = set([RankedPairs.breakWinnerTie(winners, tieBreaker)])
        
        # Return the final result
        return result
