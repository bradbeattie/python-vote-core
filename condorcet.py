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
import types, itertools

# This class determines the Condorcet winner if one exists.
class CondorcetSystem(VotingSystem):
    
    @staticmethod
    def calculate_winner(ballots):
        result = {}
        
        # Collect all candidates
        candidates = set()
        for ballot in ballots:
            if type(ballot["ballot"]) is types.DictType:
                candidates = candidates.union(ballot["ballot"].keys())
            else:
                candidates = candidates.union(item for innerlist in ballot["ballot"] for item in innerlist)
        result["candidates"] = candidates
        
        # Auto-complete each ballot (as they may omit least preferred candidates)
        for ballot in ballots:
            order_ballot = []
            
            # Convert range ballots into ordered sets
            if type(ballot["ballot"]) is types.DictType:
                while len(ballot["ballot"]) > 0:
                    most_preferred = max(ballot["ballot"].values())
                    most_preferred_candidates = set()
                    for candidate in ballot["ballot"].keys():
                        if ballot["ballot"][candidate] == most_preferred:
                            most_preferred_candidates.add(candidate)
                    order_ballot.append(most_preferred_candidates)
                    for candidate in most_preferred_candidates:
                        del ballot["ballot"][candidate]
            
            # Convert ordered arrays into ordered sets
            else:
                for candidate_group in ballot["ballot"]:
                    order_ballot.append(set(candidate_group))
            
            # Append the unreferenced candidates to the end of the ballot
            unreferenced_candidates = candidates.copy()
            for candidate_group in order_ballot:
                unreferenced_candidates = unreferenced_candidates - candidate_group
            if len(unreferenced_candidates) > 0:
                order_ballot.append(unreferenced_candidates)
            ballot["ballot"] = order_ballot

        # Generate the pairwise comparison tallies
        pairs = {}
        for pair in itertools.permutations(candidates, 2):
            pairs[pair] = 0
        for ballot in ballots:
            for candidate_group in ballot["ballot"]:
                for subsequent_candidate_group in ballot["ballot"][ballot["ballot"].index(candidate_group)+1:]:
                    for candidate in candidate_group:
                        for subsequent_candidate in subsequent_candidate_group:
                            pairs[(candidate, subsequent_candidate)] += ballot["count"]
        result["pairs"] = pairs
        
        # Filter the pairs down to the strong pairs
        keys = filter(lambda pair: pairs[(pair[0],pair[1])] > pairs[(pair[1],pair[0])], pairs)
        strong_pairs = {}
        for key in keys:
            strong_pairs[key] = pairs[key]
        result["strong_pairs"] = strong_pairs
            

        # The winner is the single candidate that never loses
        losing_candidates = set()
        for pair in strong_pairs.keys():
            losing_candidates.add(pair[1])
        winning_candidates = candidates - losing_candidates
        if len(winning_candidates) == 1:
            result["winners"] = set([list(winning_candidates)[0]])

        # Return the final result
        return result

    @staticmethod
    def __remove_weak_edges__(candidate_graph):
        edges_to_remove = []
        for edge in candidate_graph.edges():
            if candidate_graph.edge_weight(edge[0], edge[1]) <= candidate_graph.edge_weight(edge[1], edge[0]):
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            candidate_graph.del_edge(edge[0], edge[1])
        return candidate_graph
