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
    
    @staticmethod
    def condorcet_winner(ballots, notation=None):

        ballots = CondorcetSystem.convert_ballots(ballots, notation)
        candidates = CondorcetSystem.obtain_candidates(ballots)
        ballots = CondorcetSystem.complete_ballots(ballots, candidates)
        
        # Generate the pairwise comparison tallies
        pairs = {}
        for pair in itertools.permutations(candidates, 2):
            pairs[pair] = 0
        for ballot in ballots:
            for c1, r1 in ballot["ballot"].iteritems():
                for c2, r2 in ballot["ballot"].iteritems():
                    if r1 < r2:
                        pairs[(c1, c2)] += ballot["count"]

        # Filter the pairs down to the strong pairs
        keys = filter(lambda pair: pairs[(pair[0],pair[1])] > pairs[(pair[1],pair[0])], pairs)
        strong_pairs = {}
        for key in keys:
            strong_pairs[key] = pairs[key]
          
        # Prepare the result to return
        result = {
            "candidates": candidates,
            "pairs": pairs,
            "strong_pairs": strong_pairs
        }

        # The winner is the single candidate that never loses
        losing_candidates = set([pair[1] for pair in strong_pairs.keys()])
        winning_candidates = candidates - losing_candidates
        if len(winning_candidates) == 1:
            result["winners"] = set([list(winning_candidates)[0]])
        
        # Return the final result
        return result
    
    @staticmethod
    def graph_winner(graph, result):
        losing_candidates = set()
        for edge in graph.edges():
            losing_candidates.add(edge[1])
        winning_candidates = set(graph.nodes()) - losing_candidates
        
        if len(winning_candidates) == 1:
            result["winners"] = set([list(winning_candidates)[0]])
        else:
            result["tied_winners"] = set(graph.nodes())
            result["tie_breaker"] = CondorcetSystem.generate_tie_breaker(result["candidates"])
            result["winners"] = set([CondorcetSystem.break_ties(winning_candidates, result["tie_breaker"])])
        if type(list(result["winners"])[0]) == types.TupleType:
            result["winners"] = set([item for innerlist in result["winners"] for item in innerlist])
        return result
    
    @staticmethod
    def convert_ballots(ballots, notation):
        
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
            
        return ballots

        
    @staticmethod
    def obtain_candidates(ballots):
        candidates = set()
        for ballot in ballots:
            candidates |= set(ballot["ballot"].keys())
        return candidates
    
    @staticmethod
    def complete_ballots(ballots, candidates):
        for ballot in ballots:
            lowest_preference = max(ballot["ballot"].values()) + 1
            for candidate in candidates - set(ballot["ballot"].keys()):
                ballot["ballot"][candidate] = lowest_preference
        return ballots