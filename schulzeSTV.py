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

# This class implements Schulze STV, a proportional representation system
from pygraph.classes.digraph import digraph
from schulzeMethod import SchulzeMethod
import itertools

class SchulzeSTV:
    
    @staticmethod
    def calculateWinner(ballots, requiredWinners, notation=None):
        
        if notation == "preferenceSets":
            for ballot in ballots:
                newBallot = {}
                r = 0
                for rank in ballot["ballot"]:
                    r += 1
                    for candidate in rank:
                        newBallot[candidate] = r
                ballot["ballot"] = newBallot
        
        # Collect all candidates
        candidates = set()
        for ballot in ballots:
            candidates = candidates.union(ballot["ballot"].keys())
        candidates = sorted(list(candidates))
        
        managementGraph = digraph()
        managementGraph.add_nodes(itertools.combinations(candidates, requiredWinners))
        
        candidateSets = dict.fromkeys(itertools.combinations(candidates, requiredWinners + 1), 0)
        for candidateSet in candidateSets:
            for candidate in candidateSet:
                otherCandidates = sorted(list(set(candidateSet) - set([candidate])))
                completed = SchulzeSTV.__proportionalCompletion__(candidate, otherCandidates, ballots)
                weight = SchulzeSTV.__strengthOfVoteManagement__(completed)
                for subset in itertools.combinations(otherCandidates, len(otherCandidates) - 1):
                    managementGraph.add_edge(tuple(otherCandidates), tuple(sorted(list(subset) + [candidate])), weight)
        
        edgesToRemove = []
        for edge in managementGraph.edges():
            if managementGraph.edge_weight(edge[0], edge[1]) <= managementGraph.edge_weight(edge[1], edge[0]):
                edgesToRemove.append(edge)
        for edge in edgesToRemove:
            managementGraph.del_edge(edge[0], edge[1])
        
        result = {}
        managementGraph, result["actions"] = SchulzeMethod.__schwartzSetHeuristic__(managementGraph)

        # Mark the winner
        if len(managementGraph.nodes()) == 1:
            result["winners"] = set(managementGraph.nodes()[0])
        else:
            result["tiedWinners"] = set(managementGraph.nodes())
            result["tieBreaker"] = SchulzeSTV.generateTieBreaker(result["candidates"])
            result["winners"] = "Not yet sure how to break ties"
        
        return result
    
    @staticmethod
    def __proportionalCompletion__(candidate, otherCandidates, ballots):

        # Initial tally
        patternWeights = {}
        for ballot in ballots:
            pattern = []
            for otherCandidate in otherCandidates:
                if ballot["ballot"][candidate] > ballot["ballot"][otherCandidate]:
                    pattern.append(1)
                elif ballot["ballot"][candidate] == ballot["ballot"][otherCandidate]:
                    pattern.append(2)
                else:
                    pattern.append(3)
            pattern = tuple(pattern)
            if pattern not in patternWeights:
                patternWeights[pattern] = 0.0
            patternWeights[pattern] += ballot["count"]
        
        # Generate the list of patterns we need to complete
        completionPatterns = []
        numberOfOtherCandidates = len(otherCandidates)
        for i in range(0,numberOfOtherCandidates):
            for j in range(0, i+1):
                completionPatterns.append(list(set((pattern[0]) for pattern in itertools.groupby(itertools.permutations([2]*(numberOfOtherCandidates-i)+[1]*(j)+[3]*(i-j))))))
        completionPatterns = [item for innerlist in completionPatterns for item in innerlist]
        
        # Complete each pattern in order
        for completionPattern in completionPatterns:
            if completionPattern in patternWeights:
                patternWeights = SchulzeSTV.__proportionalCompletionRound__(completionPattern, patternWeights)
        return patternWeights

    @staticmethod
    def __proportionalCompletionRound__(completionPattern, patternWeights):
        
        # Remove pattern that contains indifference
        completionPatternWeight = patternWeights[completionPattern]
        del patternWeights[completionPattern]
        
        patternsToConsider = {}
        for pattern in patternWeights.keys():
            append = False
            appendTarget = []
            for i in range(len(completionPattern)):
                if completionPattern[i] != 2:
                    appendTarget.append(completionPattern[i])
                else:
                    appendTarget.append(pattern[i])
                if completionPattern[i] == 2 and pattern[i] != 2:
                    append = True
            appendTarget = tuple(appendTarget)
            if append == True:
                if appendTarget not in patternsToConsider:
                    patternsToConsider[appendTarget] = set()
                patternsToConsider[appendTarget].add(pattern)
        
        denominator = 0
        for (appendTarget, patterns) in patternsToConsider.items():
            for pattern in patterns:
                denominator += patternWeights[pattern]
        
        # Reweight the remaining items
        for pattern in patternsToConsider.keys():
            addition = sum(patternWeights[consideredPattern] for consideredPattern in patternsToConsider[pattern]) * completionPatternWeight / denominator
            if pattern not in patternWeights:
                patternWeights[pattern] = 0
            patternWeights[pattern] += addition
        return patternWeights

    # This method converts the voter profile into a capacity graph and iterates
    # on the maximum flow using the Edmonds Karp algorithm. The end result is
    # the limit of the strength of the voter management as per Markus Schulze's
    # Calcul02.pdf (draft, 28 March 2008, abstract: "In this paper we illustrate
    # the calculation of the strengths of the vote managements.").
    @staticmethod
    def __strengthOfVoteManagement__(voterProfile):
        
        
        numberOfCandidates = len(voterProfile.keys()[0])
        numberOfPatterns = len(voterProfile) - 1
        numberOfNodes = 1 + numberOfPatterns + numberOfCandidates + 1
        orderedPatterns = sorted(voterProfile.keys())
        orderedPatterns.remove(tuple([3]*numberOfCandidates))
        r = [(sum(voterProfile.values()) - voterProfile[tuple([3]*numberOfCandidates)]) / numberOfCandidates]
        
        # Generate a numberOfNodes x numberOfNodes matrix of zeroes
        C = []
        for i in range(numberOfNodes):
            C.append([0] * numberOfNodes)
            
        # Source to voters
        vertex = 0
        for pattern in orderedPatterns:
            C[0][vertex+1] = voterProfile[pattern]
            vertex += 1

        # Voters to candidates
        vertex = 0
        for pattern in orderedPatterns:
            for i in range(1,numberOfCandidates + 1):
                if pattern[i-1] == 1:
                    C[vertex+1][1 + numberOfPatterns + i - 1] = voterProfile[pattern]
            vertex += 1
        
        # Iterate towards the limit
        loop = 0
        while len(r) < 2 or r[loop-1] - r[loop] > 0.000001:
            loop += 1
            for i in range(numberOfCandidates):
                C[1 + numberOfPatterns + i][numberOfNodes - 1] = r[loop - 1]
            r.append(SchulzeSTV.__edmonds_karp__(C,0,numberOfNodes-1)/numberOfCandidates)
        return r[loop]
    

    # The Edmonds-Karp algorithm is an implementation of the Ford-Fulkerson
    # method for computing the maximum flow in a flow network in O(VE^2).
    #
    # Sourced from http://semanticweb.org/wiki/Python_implementation_of_Edmonds-Karp_algorithm
    @staticmethod
    def __edmonds_karp__(C, source, sink):
        n = len(C) # C is the capacity matrix
        F = [[0] * n for i in xrange(n)]
        # residual capacity from u to v is C[u][v] - F[u][v]

        while True:
            path = SchulzeSTV.__bfs__(C, F, source, sink)
            if not path:
                break
            # traverse path to find smallest capacity
            flow = min(C[u][v] - F[u][v] for u,v in path)
            # traverse path to update flow
            for u,v in path:
                F[u][v] += flow
                F[v][u] -= flow
                
        return sum(F[source][i] for i in xrange(n))
    
    # In graph theory, breadth-first search (BFS) is a graph search algorithm
    # that begins at the root node and explores all the neighboring nodes. Then
    # for each of those nearest nodes, it explores their unexplored neighbor
    # nodes, and so on, until it finds the goal.
    #
    # Sourced from http://semanticweb.org/wiki/Python_implementation_of_Edmonds-Karp_algorithm    
    @staticmethod
    def __bfs__(C, F, source, sink):
        queue = [source]                 
        paths = {source: []}
        while queue:
            u = queue.pop(0)
            for v in xrange(len(C)):
                if C[u][v] - F[u][v] > 0 and v not in paths:
                    paths[v] = paths[u] + [(u,v)]
                    if v == sink:
                        return paths[v]
                    queue.append(v)
        return None