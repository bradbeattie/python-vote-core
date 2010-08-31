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
import math, copy

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
        quota = self.quota
        remaining_candidates = copy.deepcopy(self.candidates)
        ballots = copy.deepcopy(self.ballots)
        
        # Loop until we have enough candidates
        while len(self.winners) < self.required_winners and len(remaining_candidates) + len(self.winners) > self.required_winners:
            
            # If all the votes have been used up, start from scratch for the remaining candidates
            round = {}
            if len(filter(lambda ballot: ballot["count"] > 0, ballots)) == 0:
                round["note"] = "reset"
                ballots = copy.deepcopy(self.ballots)
                for ballot in ballots:
                    ballot["ballot"] = filter(lambda x: x in remaining_candidates, ballot["ballot"])
                quota = STV.droop_quota(ballots, self.required_winners - len(self.winners))
            
            # If any candidates meet or exceeds the quota, they're a winner
            round["tallies"] = STV.tallies(ballots)
            if max(round["tallies"].values()) >= quota:
                
                # Collect candidates as winners
                round["winners"] = set([
                    candidate
                    for candidate, tally in round["tallies"].items()
                    if tally >= self.quota
                ])
                self.winners |= round["winners"]
                remaining_candidates -= round["winners"]
            
                # Redistribute excess votes
                for ballot in ballots:
                    if ballot["ballot"][0] in round["winners"]:
                        ballot["count"] *= (round["tallies"][ballot["ballot"][0]] - self.quota) / round["tallies"][ballot["ballot"][0]]

                # Remove candidates from remaining ballots
                ballots = STV.remove_candidates_from_ballots(round["winners"], ballots)
        
            # If no candidate exceeds the quota, elimiate the least preferred
            else:
                round.update(self.loser(round["tallies"]))
                remaining_candidates.remove(round["loser"])
                ballots = STV.remove_candidates_from_ballots([round["loser"]], ballots)
            
            # Record this round's actions
            self.rounds.append(round)

        # Append the final winner and return
        if len(self.winners) < self.required_winners:
            self.remaining_candidates = remaining_candidates
            self.winners |= self.remaining_candidates

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
    def tallies(ballots):
        tallies = dict.fromkeys(STV.viable_candidates(ballots), 0)
        for ballot in ballots:
            if len(ballot["ballot"]) > 0:
                tallies[ballot["ballot"][0]] += ballot["count"]
        return dict((candidate,votes) for (candidate,votes) in tallies.iteritems() if votes > 0) 
    
    @staticmethod
    def viable_candidates(ballots):
        candidates = set([])
        for ballot in ballots:
            candidates |= set(ballot["ballot"])
        return candidates
    
    @staticmethod
    def droop_quota(ballots, seats = 1):
        voters = 0;
        for ballot in ballots:
            voters += ballot["count"]
        return int(math.floor(voters / (seats + 1)) + 1)

    def results(self):
        results = VotingSystem.results(self)
        results["quota"] = self.quota
        if hasattr(self, 'rounds'):
            results["rounds"] = self.rounds
        if hasattr(self, 'remaining_candidates'):
            results["remaining_candidates"] = self.remaining_candidates
        return results