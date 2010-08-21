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
import itertools, types

# This class determines the Condorcet winner if one exists.
class CondorcetSystem(VotingSystem):
    
    def __init__(self, ballots, notation = None):
        self.convert_ballots(ballots, notation)
        VotingSystem.__init__(self)
    
    def calculate_results(self):
        
        # Generate the pairwise comparison tallies
        self.pairs = {}
        for pair in itertools.permutations(self.candidates, 2):
            self.pairs[pair] = 0
        for ballot in self.ballots:
            for c1, r1 in ballot["ballot"].iteritems():
                for c2, r2 in ballot["ballot"].iteritems():
                    if r1 < r2:
                        self.pairs[(c1, c2)] += ballot["count"]

        # Filter the pairs down to the strong pairs
        keys = filter(lambda pair: self.pairs[(pair[0],pair[1])] > self.pairs[(pair[1],pair[0])], self.pairs)
        self.strong_pairs = {}
        for key in keys:
            self.strong_pairs[key] = self.pairs[key]
          
        # The winner is the single candidate that never loses
        losing_candidates = set([pair[1] for pair in self.strong_pairs.keys()])
        winning_candidates = self.candidates - losing_candidates
        if len(winning_candidates) == 1:
            self.winners = set([list(winning_candidates)[0]])

    def results(self):
        results = {
            "candidates": self.candidates,
            "pairs": self.pairs,
            "strong_pairs": self.strong_pairs,
            "winners": self.winners,
        }
        return results
    
    def graph_winner(self):
        losing_candidates = set()
        for edge in self.graph.edges():
            losing_candidates.add(edge[1])
        winning_candidates = set(self.graph.nodes()) - losing_candidates
        
        if len(winning_candidates) == 1:
            self.winners = set([list(winning_candidates)[0]])
        else:
            self.tied_winners = set(self.graph.nodes())
            self.winners = set([self.break_ties(winning_candidates)])
        if type(list(self.winners)[0]) == types.TupleType:
            self.winners = set([item for innerlist in self.winners for item in innerlist])
    
    def convert_ballots(self, ballots, notation):
        
        if notation == "grouping":
            if type(ballots[0]["ballot"][0]) != types.ListType:
                raise Exception("Grouping notation expects double-nested lists")
            for ballot in ballots:
                new_ballot = {}
                r = 0
                for rank in ballot["ballot"]:
                    r += 1
                    for candidate in rank:
                        new_ballot[candidate] = r
                ballot["ballot"] = new_ballot
        
        elif notation == "rating":
            for ballot in ballots:
                for candidate, rating in ballot["ballot"].iteritems():
                    ballot["ballot"][candidate] = -float(rating)

        elif notation != "ranking":
            raise Exception("Unknown notation specified")
        
        self.candidates = set()
        for ballot in ballots:
            self.candidates |= set(ballot["ballot"].keys())
        
        for ballot in ballots:
            lowest_preference = max(ballot["ballot"].values()) + 1
            for candidate in self.candidates - set(ballot["ballot"].keys()):
                ballot["ballot"][candidate] = lowest_preference
        
        self.ballots = ballots