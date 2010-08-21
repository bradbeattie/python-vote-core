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
import copy, types

# This class implements plurality at large (aka block voting).
class PluralityAtLarge(VotingSystem):
    
    def __init__(self, ballots, required_winners = 1):
        self.required_winners = required_winners
        self.convert_ballots(ballots)
        
        # Ensure we have sufficient candidates
        if len(self.candidates) < required_winners:
            raise Exception("Insufficient candidates to meet produce sufficient winners")
        
        VotingSystem.__init__(self)
        
    def convert_ballots(self, ballots):
        
        # Parse the incoming candidate list
        self.candidates = set()
        for ballot in ballots:
            
            # Convert single candidate ballots into ballot lists
            if type(ballot["ballot"]) != types.ListType:
                ballot["ballot"] = [ballot["ballot"]]
                
            # Ensure no ballot has an excess of candidates
            if len(ballot["ballot"]) > self.required_winners:
                raise Exception("A ballot contained too many candidates")
            
            # Observe all mentioned candidates 
            for candidate in ballot["ballot"]:
                self.candidates.add(candidate)

        self.ballots = ballots


    def calculate_results(self):
        
        # Sum up all votes for each candidate
        tallies = dict.fromkeys(self.candidates, 0)
        for ballot in self.ballots:
            for candidate in ballot["ballot"]:
                tallies[candidate] += ballot["count"]
        self.tallies = copy.deepcopy(tallies)
        
        # Determine which candidates win
        winning_candidates = set()
        while len(winning_candidates) < self.required_winners:
            
            # Find the remaining candidates with the most votes
            largest_tally = max(tallies.values())
            top_candidates = self.matching_keys(tallies, largest_tally)
            
            # Reduce the found candidates if there are too many
            if len(top_candidates | winning_candidates) > self.required_winners:
                self.tied_winners = top_candidates.copy()
                while len(top_candidates | winning_candidates) > self.required_winners:
                    top_candidates.remove(self.break_ties(top_candidates, True))
            
            # Move the top candidates into the winning pile
            winning_candidates |= top_candidates
            for candidate in top_candidates:
                del tallies[candidate]
                
        # Return the final result
        self.winners =  winning_candidates

    def results(self):
        results = VotingSystem.results(self)
        results["tallies"] = self.tallies
        if hasattr(self, 'tied_winners'):
            results["tied_winners"] = self.tied_winners
        return results