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
import types, itertools

# This class determines the Condorcet winner if one exists.
class CondorcetSystem(VotingSystem):
    
    @staticmethod
    def calculateWinner(ballots):
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
            orderBallot = []
            
            # Convert range ballots into ordered sets
            if type(ballot["ballot"]) is types.DictType:
                while len(ballot["ballot"]) > 0:
                    mostPreferred = max(ballot["ballot"].values())
                    mostPreferredCandidates = set()
                    for candidate in ballot["ballot"].keys():
                        if ballot["ballot"][candidate] == mostPreferred:
                            mostPreferredCandidates.add(candidate)
                    orderBallot.append(mostPreferredCandidates)
                    for candidate in mostPreferredCandidates:
                        del ballot["ballot"][candidate]
            
            # Convert ordered arrays into ordered sets
            else:
                for candidateGroup in ballot["ballot"]:
                    orderBallot.append(set(candidateGroup))
            
            # Append the unreferenced candidates to the end of the ballot
            unreferencedCandidates = candidates.copy()
            for candidateGroup in orderBallot:
                unreferencedCandidates = unreferencedCandidates - candidateGroup
            if len(unreferencedCandidates) > 0:
                orderBallot.append(unreferencedCandidates)
            ballot["ballot"] = orderBallot

        # Generate the pairwise comparison tallies
        pairs = {}
        for pair in itertools.permutations(candidates, 2):
            pairs[pair] = 0
        for ballot in ballots:
            for candidateGroup in ballot["ballot"]:
                for subsequentCandidateGroup in ballot["ballot"][ballot["ballot"].index(candidateGroup)+1:]:
                    for candidate in candidateGroup:
                        for subsequentCandidate in subsequentCandidateGroup:
                            pairs[(candidate, subsequentCandidate)] += ballot["count"]
        result["pairs"] = pairs
        
        # Filter the pairs down to the strong pairs
        keys = filter(lambda pair: pairs[(pair[0],pair[1])] > pairs[(pair[1],pair[0])], pairs)
        strongPairs = {}
        for key in keys:
            strongPairs[key] = pairs[key]
        result["strongPairs"] = strongPairs
            

        # The winner is the single candidate that never loses
        losingCandidates = set()
        for pair in strongPairs.keys():
            losingCandidates.add(pair[1])
        winningCandidates = candidates - losingCandidates
        if len(winningCandidates) == 1:
            result["winners"] = set([list(winningCandidates)[0]])

        # Return the final result
        return result

    @staticmethod
    def __removeWeakEdges__(candidateGraph):
        edgesToRemove = []
        for edge in candidateGraph.edges():
            if candidateGraph.edge_weight(edge[0], edge[1]) <= candidateGraph.edge_weight(edge[1], edge[0]):
                edgesToRemove.append(edge)
        for edge in edgesToRemove:
            candidateGraph.del_edge(edge[0], edge[1])
        return candidateGraph
