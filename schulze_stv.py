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
from schulze_method import SchulzeMethod
from condorcet import CondorcetSystem
from voting_system import VotingSystem
import itertools

class SchulzeSTV(VotingSystem):

    @staticmethod
    def calculate_winner(ballots, required_winners, notation="ranking"):
        
        # Standardize the incoming data
        ballots = CondorcetSystem.convert_ballots(ballots, notation)
        candidates = CondorcetSystem.obtain_candidates(ballots)
        ballots = CondorcetSystem.complete_ballots(ballots, candidates)
        result = {"candidates": candidates}
        
        # Build the graph of possible winners
        graph = digraph()
        for candidate_set in itertools.combinations(candidates, required_winners):
            graph.add_nodes([tuple(sorted(list(candidate_set)))])
        
        # Generate the edges between nodes
        for candidate_set in itertools.combinations(candidates, required_winners + 1):
            for candidate in candidate_set:
                other_candidates = sorted(list(set(candidate_set) - set([candidate])))
                completed = SchulzeSTV.__proportional_completion__(candidate, other_candidates, ballots)
                weight = SchulzeSTV.__strength_of_vote_management__(completed)
                for subset in itertools.combinations(other_candidates, len(other_candidates) - 1):
                    graph.add_edge(tuple(other_candidates), tuple(sorted(list(subset) + [candidate])), weight)
                
        # Determine the winner through the Schwartz set heuristic
        graph, result["actions"] = SchulzeMethod.schwartz_set_heuristic(graph)
        return CondorcetSystem.graph_winner(graph, result)
    
    @staticmethod
    def __proportional_completion__(candidate, other_candidates, ballots):
        
        # Ensure each pattern is represented
        profile = {}
        for i in range(0,len(other_candidates) + 1):
            for pattern in itertools.permutations([1]*(len(other_candidates)-i)+[3]*(i)):
                profile[pattern] = 0
                    
        # Obtain an initial tally from the ballots
        for ballot in ballots:
            pattern = []
            for other_candidate in other_candidates:
                if ballot["ballot"][candidate] > ballot["ballot"][other_candidate]:
                    pattern.append(1)
                elif ballot["ballot"][candidate] == ballot["ballot"][other_candidate]:
                    pattern.append(2)
                else:
                    pattern.append(3)
            pattern = tuple(pattern)
            if pattern not in profile:
                profile[pattern] = 0.0
            profile[pattern] += ballot["count"]
            
        # Generate the list of patterns we need to complete
        completion_patterns = []
        for i in range(0,len(other_candidates)):
            for j in range(0, i+1):
                completion_patterns.append(list(set((pattern[0]) for pattern in itertools.groupby(itertools.permutations([2]*(len(other_candidates)-i)+[1]*(j)+[3]*(i-j))))))
        print completion_patterns
        completion_patterns = [item for innerlist in completion_patterns for item in innerlist]
        
        # Complete each pattern in order
        for pattern in completion_patterns:
            if pattern in profile:
                profile = SchulzeSTV.__proportional_completion_round__(pattern, profile)
        
        return profile

    @staticmethod
    def __proportional_completion_round__(completion_pattern, profile):
        
        # Remove pattern that contains indifference
        completion_pattern_weight = profile[completion_pattern]
        del profile[completion_pattern]
        
        patterns_to_consider = {}
        for pattern in profile.keys():
            append = False
            append_target = []
            for i in range(len(completion_pattern)):
                if completion_pattern[i] != 2:
                    append_target.append(completion_pattern[i])
                else:
                    append_target.append(pattern[i])
                if completion_pattern[i] == 2 and pattern[i] != 2:
                    append = True
            append_target = tuple(append_target)
            if append == True:
                if append_target not in patterns_to_consider:
                    patterns_to_consider[append_target] = set()
                patterns_to_consider[append_target].add(pattern)
        
        denominator = 0
        for (append_target, patterns) in patterns_to_consider.items():
            for pattern in patterns:
                denominator += profile[pattern]
        
        # Reweight the remaining items
        for pattern in patterns_to_consider.keys():
            if denominator == 0:
                profile[pattern] += completion_pattern_weight / len(patterns_to_consider[pattern])
            else:
                if pattern not in profile:
                    profile[pattern] = 0
                profile[pattern] += sum(profile[considered_pattern] for considered_pattern in patterns_to_consider[pattern]) * completion_pattern_weight / denominator
        return profile

    # This method converts the voter profile into a capacity graph and iterates
    # on the maximum flow using the Edmonds Karp algorithm. The end result is
    # the limit of the strength of the voter management as per Markus Schulze's
    # Calcul02.pdf (draft, 28 March 2008, abstract: "In this paper we illustrate
    # the calculation of the strengths of the vote managements.").
    @staticmethod
    def __strength_of_vote_management__(voter_profile):
        
        number_of_candidates = len(voter_profile.keys()[0])
        number_of_patterns = len(voter_profile) - 1
        number_of_nodes = 1 + number_of_patterns + number_of_candidates + 1
        ordered_patterns = sorted(voter_profile.keys())
        ordered_patterns.remove(tuple([3]*number_of_candidates))
        
        r = [(float(sum(voter_profile.values())) - voter_profile[tuple([3]*number_of_candidates)]) / number_of_candidates]
        
        # Generate a number_of_nodes x number_of_nodes matrix of zeroes
        C = []
        for i in range(number_of_nodes):
            C.append([0] * number_of_nodes)
            
        # Source to voters
        vertex = 0
        for pattern in ordered_patterns:
            C[0][vertex+1] = voter_profile[pattern]
            vertex += 1

        # Voters to candidates
        vertex = 0
        for pattern in ordered_patterns:
            for i in range(1,number_of_candidates + 1):
                if pattern[i-1] == 1:
                    C[vertex+1][1 + number_of_patterns + i - 1] = voter_profile[pattern]
            vertex += 1
        
        # Iterate towards the limit
        while len(r) < 2 or r[-2] - r[-1] > 0.0000001:
            for i in range(number_of_candidates):
                C[1 + number_of_patterns + i][number_of_nodes - 1] = r[-1]
            r.append(SchulzeSTV.__edmonds_karp__(C,0,number_of_nodes-1)/number_of_candidates)
        return r[-1]
    

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