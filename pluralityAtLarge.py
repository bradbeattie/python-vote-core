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

from votingSystem import VotingSystem
import copy, types
class PluralityAtLarge(VotingSystem):
    
    @staticmethod
    def calculateWinner(ballots, requiredWinners = 1):
        result = {}
        
        # Parse the incoming candidate list
        candidates = set()
        for ballot in ballots:
            
            # Convert single candidate ballots into ballot lists
            if type(ballot["ballot"]) != types.ListType:
                ballot["ballot"] = [ballot["ballot"]]
                
            # Ensure no ballot has an excess of candidates
            if len(ballot["ballot"]) > requiredWinners:
                raise Exception("A ballot contained too many candidates")
            
            # Observe all mentioned candidates 
            for candidate in ballot["ballot"]:
                candidates.add(candidate)
        
        # Ensure we have sufficient candidates
        if len(candidates) < requiredWinners:
            raise Exception("Insufficient candidates to meet produce sufficient winners")
        
        # Generate tie breaker, which may or may not be used later
        tieBreaker = PluralityAtLarge.generateTieBreaker(candidates)

        # Sum up all votes for each candidate
        tallies = dict.fromkeys(candidates, 0)
        for ballot in ballots:
            for candidate in ballot["ballot"]:
                tallies[candidate] += ballot["count"]
        result["tallies"] = copy.deepcopy(tallies)
        
        # Determine which candidates win
        winningCandidates = set()
        print requiredWinners
        while len(winningCandidates) < requiredWinners:
            
            # Find the remaining candidates with the most votes
            topCandidates = set()
            largestTally = max(tallies.values())
            for candidate, tally in tallies.iteritems():
                if tally == largestTally:
                    topCandidates.add(candidate)
            
            # Reduce the found candidates if there are too many
            if len(topCandidates | winningCandidates) > requiredWinners:
                result["tieBreaker"] = tieBreaker
                result["tiedWinners"] = topCandidates.copy()
                while len(topCandidates | winningCandidates) > requiredWinners:
                    topCandidates.remove(PluralityAtLarge.breakLoserTie(topCandidates, tieBreaker))
            
            # Move the top candidates into the winning pile
            winningCandidates |= topCandidates
            for candidate in topCandidates:
                del tallies[candidate]
                
        # Return the final result
        result["winners"] = winningCandidates
        return result