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
import math, copy
class InstantRunoffVote(VotingSystem):
    
    @staticmethod
    def calculateWinner(ballots):
        result = {"rounds": []}
        
        # Determine the number of votes necessary to win
        quota = 0;
        for ballot in ballots:
            quota += ballot["count"]
        quota = int(math.floor(quota / 2) + 1);
        result["quota"] = quota
        
        # Collect the list of candidates
        candidates = set()
        for ballot in ballots:
            candidates.add(ballot["ballot"][0])
        
        # Generate tie breaker
        tieBreaker = InstantRunoffVote.generateTieBreaker(candidates)

        # Loop until a candidate has obtained a majority of votes
        tallies = {}
        while len(tallies) == 0 or max(tallies.values()) < quota:
            round = {}
            
            # Elimination step
            if len(tallies) > 0:

                # Determine which candidates have the fewest votes
                fewestVotes = min(tallies.values())
                leastPreferredCandidates = set()
                for candidate in tallies.keys():
                    if tallies[candidate] == fewestVotes:
                        leastPreferredCandidates.add(candidate)
                if len(leastPreferredCandidates) > 1:
                    result["tieBreaker"] = tieBreaker
                    round["tiedLosers"] = leastPreferredCandidates
                    loser = InstantRunoffVote.breakLoserTie(leastPreferredCandidates, tieBreaker)
                    
                else:
                    loser = list(leastPreferredCandidates)[0]
                round["loser"] = loser
                
                # Eliminate references to the lost candidate
                candidates.remove(loser)
                for ballot in ballots:
                    if loser in ballot["ballot"]:
                        ballot["ballot"].remove(loser)
                        
                result["rounds"].append(round)
                round["tallies"] = copy.deepcopy(tallies)
                        
            # Sum up all votes for each candidate
            tallies = dict.fromkeys(candidates, 0)
            for ballot in ballots:
                if len(ballot["ballot"]) > 0:
                    tallies[ballot["ballot"][0]] +=  ballot["count"]
            
        # Append the final winner and return
        result["winners"] = set([max(tallies, key=tallies.get)])
        return result