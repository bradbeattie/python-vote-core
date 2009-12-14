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
class SingleTransferableVote(VotingSystem):
    
    @staticmethod
    def calculateWinner(ballots, requiredWinners = 1):
                
        # We might need to split ballots into fractions
        for ballot in ballots:
            ballot["count"] = float(ballot["count"])
            
        # Collect the list of candidates
        candidates = set()
        for ballot in ballots:
            for candidate in ballot["ballot"]:
                candidates.add(candidate)
        if len(candidates) < requiredWinners:
            raise Exception("Insufficient number of candidates")
        elif len(candidates) == requiredWinners:
            return {"winners":candidates}
        
        # Generate tie breaker
        tieBreaker = SingleTransferableVote.generateTieBreaker(candidates)
        
        # Loop until a candidate has obtained a majority of votes
        result = {"rounds": [], "winners": set()}
        while len(result["winners"]) < requiredWinners:
            round = {}
            
            # Remove any zero-strength ballots
            for ballot in ballots:
                if len(ballot["ballot"]) == 0 or ballot["count"] == 0:
                    ballots.remove(ballot)
            
            # Sum up all votes for each candidate
            tallies = dict.fromkeys(candidates, 0)
            for ballot in ballots:
                tallies[ballot["ballot"][0]] += ballot["count"]
            round["tallies"] = copy.deepcopy(tallies)
            
            # Determine the number of votes necessary to win (Droop Quota)
            quota = 0;
            for ballot in ballots:
                quota += ballot["count"]
            quota = int(math.floor(quota / (requiredWinners - len(result["winners"]) + 1)) + 1)
            round["quota"] = quota
            
            # If any candidates meet or exceeds the quota
            if max(tallies.values()) >= quota:
                
                # Collect candidates as winners
                round["winners"] = set()
                for candidate in tallies.keys():
                    if tallies[candidate] >= quota:
                        round["winners"].add(candidate)
                        result["winners"].add(candidate)
            
                # Redistribute excess votes
                for ballot in ballots:
                    if ballot["ballot"][0] in round["winners"]:
                        ballot["count"] *= (tallies[ballot["ballot"][0]] - quota) / tallies[ballot["ballot"][0]]
        
                # Remove candidates from remaining ballots
                for candidate in round["winners"]:
                    candidates.remove(candidate)
                for ballot in ballots:
                    for candidate in round["winners"]:
                        if candidate in ballot["ballot"]:
                            ballot["ballot"].remove(candidate)
        
            # If no ballots were redistributed
            else:

                # Determine which candidates have the fewest votes
                fewestVotes = min(tallies.values())
                leastPreferredCandidates = set()
                for candidate in tallies.keys():
                    if tallies[candidate] == fewestVotes:
                        leastPreferredCandidates.add(candidate)
                if len(leastPreferredCandidates) > 1:
                    result["tieBreaker"] = tieBreaker
                    round["tiedLosers"] = leastPreferredCandidates
                    round["loser"] = SingleTransferableVote.breakLoserTie(leastPreferredCandidates, tieBreaker)
                else:
                    round["loser"] = list(leastPreferredCandidates)[0]
                    
                
                # Eliminate references to the lost candidate
                candidates.remove(round["loser"])
                for ballot in ballots:
                    if round["loser"] in ballot["ballot"]:
                        ballot["ballot"].remove(round["loser"])
            
            result["rounds"].append(round)

        # Append the final winner and return
        return result