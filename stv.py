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
import math
import copy

# This class implements the Single Transferable vote (aka STV) in its most
# classic form (see http://en.wikipedia.org/wiki/Single_transferable_vote).
# Alternate counting methods such as Meek's and Warren's would be nice, but
# would need to be covered in a separate class.
class STV(VotingSystem):
    
    def __init__(self, ballots, required_winners = 1):
        self.ballots = ballots
        self.candidates = STV.viable_candidates(ballots)
        self.quota = STV.droop_quota(ballots, required_winners)
        self.required_winners = required_winners
        for ballot in ballots:
            ballot["count"] = float(ballot["count"])
        VotingSystem.__init__(self)
    
    def calculate_results(self):
        
        self.rounds = []
        self.winners = set()
        candidates = copy.deepcopy(self.candidates)
        ballots = copy.deepcopy(self.ballots)
        
        # Loop until we have enough candidates
        while len(self.winners) < self.required_winners and len(candidates) + len(self.winners) > self.required_winners:
            
            
            # Sum up all votes for each candidate
            round = {"tallies": STV.tallies(ballots)}
            
            # If any candidates meet or exceeds the quota
            if max(round["tallies"].values()) >= self.quota:
                
                # Collect candidates as winners
                round["winners"] = set()
                for (candidate,tally) in round["tallies"].items():
                    if tally >= self.quota:
                        round["winners"].add(candidate)
                self.winners |= round["winners"]
            
                # Redistribute excess votes
                for ballot in ballots:
                    if ballot["ballot"][0] in round["winners"]:
                        ballot["count"] *= (round["tallies"][ballot["ballot"][0]] - self.quota) / round["tallies"][ballot["ballot"][0]]
        
                # Remove candidates from remaining ballots
                candidates -= round["winners"]
                ballots = STV.remove_candidates_from_ballots(round["winners"], ballots)
        
            # If no ballots were redistributed
            else:
                # Eliminate references to the losing candidate
                round.update(self.loser(round["tallies"]))
                candidates.remove(round["loser"])
                ballots = STV.remove_candidates_from_ballots([round["loser"]], ballots)
            
            self.rounds.append(round)

        # Append the final winner and return
        if len(self.winners) < self.required_winners:
            self.remaining_candidates = candidates
            for candidate in candidates:
                self.winners.add(candidate)

    def loser(self, tallies):
        losers = self.matching_keys(tallies, min(tallies.values()))
        if len(losers) == 1:
            return {"loser": list(losers)[0]}
        else:
            return {
                "tied_losers": losers,
                "loser": self.break_ties(losers, True)
            }
            
    @staticmethod
    def remove_candidates_from_ballots(candidates, ballots):
        for ballot in ballots:
            for candidate in candidates:
                if candidate in ballot["ballot"]:
                    ballot["ballot"].remove(candidate)
        return ballots
            
    @staticmethod
    def viable_candidates(ballots):
        return set([ballot["ballot"][0] for ballot in ballots if len(ballot["ballot"]) > 0])
    
    @staticmethod
    def tallies(ballots):
        tallies = dict.fromkeys(STV.viable_candidates(ballots), 0)
        for ballot in ballots:
            if len(ballot["ballot"]) > 0:
                tallies[ballot["ballot"][0]] += ballot["count"]
        return tallies
    
    @staticmethod
    def droop_quota(ballots, seats = 1):
        quota = 0;
        for ballot in ballots:
            quota += ballot["count"]
        return int(math.floor(quota / (seats + 1)) + 1)

    def results(self):
        results = VotingSystem.results(self)
        results["quota"] = self.quota
        if hasattr(self, 'rounds'):
            results["rounds"] = self.rounds
        if hasattr(self, 'remaining_candidates'):
            results["remaining_candidates"] = self.remaining_candidates
        return results