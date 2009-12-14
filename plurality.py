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
import types
class Plurality(VotingSystem):
    
    @staticmethod
    def calculateWinner(ballots):
        result = {}
        
        # Collect the list of candidates
        candidates = set()
        for ballot in ballots:
            if type(ballot["ballot"]) == types.ListType:
                ballot["ballot"] = ballot["ballot"][0] 
            candidates.add(ballot["ballot"])
            
        # Generate tie breaker
        tieBreaker = Plurality.generateTieBreaker(candidates)

        # Sum up all votes for each candidate
        tallies = dict.fromkeys(candidates, 0)
        for ballot in ballots:
            tallies[ballot["ballot"]] +=  ballot["count"]
        result["tallies"] = tallies
        
        # Determine who got the most votes
        winners = set()
        mostVotes = max(tallies.values())
        for candidate, votes in tallies.iteritems():
            if votes == mostVotes:
                winners.add(candidate)
        
        # Mark the winner
        if len(winners) == 1:
            result["winners"] = winners
        else:
            result["tiedWinners"] = winners
            result["tieBreaker"] = tieBreaker
            result["winners"] = set([Plurality.breakWinnerTie(winners, tieBreaker)])
        
        # Return the final result
        return result