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

from voting_system import VotingSystem
import copy

# This class implements the Single Transferable vote (aka STV) in its most
# classic form (see http://en.wikipedia.org/wiki/Single_transferable_vote).
# Alternate counting methods such as Meek's and Warren's would be nice, but
# would need to be covered in a separate class.
class STV(VotingSystem):
    
    @staticmethod
    def calculate_winner(ballots, required_winners = 1):
                
        # We might need to split ballots into fractions
        for ballot in ballots:
            ballot["count"] = float(ballot["count"])
            
        # Collect the list of candidates
        candidates = set()
        for ballot in ballots:
            for candidate in ballot["ballot"]:
                candidates.add(candidate)
        if len(candidates) < required_winners:
            raise Exception("Insufficient number of candidates")
        elif len(candidates) == required_winners:
            return {"winners":candidates}
        
        # Determine the number of votes necessary to win (Droop Quota)
        result = {
            "quota": STV.droop_quota(ballots, required_winners),
            "rounds": [],
            "winners": set(),
        }
        
        # Generate tie breaker
        tie_breaker = STV.generate_tie_breaker(candidates)
        
        # Loop until we have enough candidates or has obtained a majority of votes
        while len(result["winners"]) < required_winners and len(candidates) + len(result["winners"]) > required_winners:
            
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
                fewest_votes = min(round["tallies"].values())
                least_preferred_candidates = STV.matching_keys(round["tallies"], fewest_votes)
                if len(least_preferred_candidates) > 1:
                    result["tie_breaker"] = tie_breaker
                    round["tied_losers"] = least_preferred_candidates
                    round["loser"] = STV.break_ties(least_preferred_candidates, tie_breaker, True)
                else:
                    round["loser"] = list(least_preferred_candidates)[0]
                    
                
                # Eliminate references to the lost candidate
                candidates.remove(round["loser"])
                for ballot in ballots:
                    if round["loser"] in ballot["ballot"]:
                        ballot["ballot"].remove(round["loser"])
            
            result["rounds"].append(round)

        # Append the final winner and return
        if len(result["winners"]) < required_winners:
            result["remaining_candidates"] = candidates
            for candidate in candidates:
                result["winners"].add(candidate)
        return result
