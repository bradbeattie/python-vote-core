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
import copy

# This class implements the Single Transferable vote (aka STV) in its most
# classic form (see http://en.wikipedia.org/wiki/Single_transferable_vote).
# Alternate counting methods such as Meek's and Warren's would be nice, but
# would need to be covered in a separate class.
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
        
        # Determine the number of votes necessary to win (Droop Quota)
        result = {
            "quota": SingleTransferableVote.droopQuota(ballots, requiredWinners),
            "rounds": [],
            "winners": set(),
        }
        
        # Generate tie breaker
        tieBreaker = SingleTransferableVote.generateTieBreaker(candidates)
        
        # Loop until we have enough candidates or has obtained a majority of votes
        while len(result["winners"]) < requiredWinners and len(candidates) + len(result["winners"]) > requiredWinners:
            
            # Remove any zero-strength ballots
            for ballot in copy.deepcopy(ballots):
                if len(ballot["ballot"]) == 0 or ballot["count"] == 0:
                    ballots.remove(ballot)
            
            # Sum up all votes for each candidate
            round = {"tallies": dict.fromkeys(candidates, 0)}
            for ballot in ballots:
                round["tallies"][ballot["ballot"][0]] += ballot["count"]
            
            # If any candidates meet or exceeds the quota
            if max(round["tallies"].values()) >= result["quota"]:
                
                # Collect candidates as winners
                round["winners"] = set()
                for (candidate,tally) in round["tallies"].items():
                    if tally >= result["quota"]:
                        round["winners"].add(candidate)
                result["winners"] |= round["winners"]
            
                # Redistribute excess votes
                for ballot in ballots:
                    if ballot["ballot"][0] in round["winners"]:
                        ballot["count"] *= (round["tallies"][ballot["ballot"][0]] - result["quota"]) / round["tallies"][ballot["ballot"][0]]
        
                # Remove candidates from remaining ballots
                candidates -= round["winners"]
                for ballot in ballots:
                    for candidate in round["winners"]:
                        if candidate in ballot["ballot"]:
                            ballot["ballot"].remove(candidate)
        
            # If no ballots were redistributed
            else:

                # Determine which candidates have the fewest votes
                fewestVotes = min(round["tallies"].values())
                leastPreferredCandidates = set((candidate) for (candidate,votes) in round["tallies"].iteritems() if votes == fewestVotes)
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
        if len(result["winners"]) < requiredWinners:
            result["remainingCandidates"] = candidates
            for candidate in candidates:
                result["winners"].add(candidate)
        return result