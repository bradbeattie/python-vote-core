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

# This class implements instant-runoff voting (aka IRV, alternative vote, etc).
class IRV(VotingSystem):
    
    @staticmethod
    def calculate_winner(ballots):
        
        # Determine the number of votes necessary to win
        result = {
            "quota": IRV.droop_quota(ballots, 1),
            "rounds": []
        }
        
        # Collect the list of candidates
        candidates = set([ballot["ballot"][0] for ballot in ballots])
        
        # Generate tie breaker
        tie_breaker = IRV.generate_tie_breaker(candidates)

        # Loop until a candidate has obtained a majority of votes
        tallies = {}
        while len(tallies) == 0 or max(tallies.values()) < result["quota"] or len(candidates) == 1:
            round = {}
            
            # Elimination step
            if len(tallies) > 0:

                # Determine which candidates have the fewest votes
                fewest_votes = min(tallies.values())
                losers = IRV.matching_keys(tallies, fewest_votes)
                if len(losers) > 1:
                    result["tie_breaker"] = tie_breaker
                    round["tied_losers"] = losers
                    loser = IRV.break_ties(losers, tie_breaker, True)
                    
                else:
                    loser = list(losers)[0]
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
        if len(candidates) == 1:
            result["winners"] = list(candidates)[0]
        else:
            result["winners"] = set([max(tallies, key=tallies.get)])
        return result
