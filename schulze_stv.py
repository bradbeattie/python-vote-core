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
from pygraph.algorithms.minmax import maximum_flow
from schulze_method import SchulzeMethod
import itertools

class SchulzeSTV(SchulzeMethod):
    
    def __init__(self, ballots, required_winners, notation = None):
        self.required_winners = required_winners
        SchulzeMethod.__init__(self, ballots, notation)
        
    def calculate_results(self):
        
        # Generate the list of patterns we need to complete
        self.__generate_completion_patterns__()
        self.__generate_completed_patterns__()
    
        # Build the graph of possible winners
        self.graph = digraph()
        for candidate_set in itertools.combinations(self.candidates, self.required_winners):
            self.graph.add_nodes([tuple(sorted(list(candidate_set)))])

        self.__generate_vote_management_graph__()
        
        # Generate the edges between nodes
        for candidate_set in itertools.combinations(self.candidates, self.required_winners + 1):
            for candidate in candidate_set:
                other_candidates = sorted(list(set(candidate_set) - set([candidate])))
                completed = self.__proportional_completion__(candidate, other_candidates)
                weight = self.__strength_of_vote_management__(completed)
                if weight > 0:
                    for subset in itertools.combinations(other_candidates, len(other_candidates) - 1):
                        self.graph.add_edge((tuple(other_candidates), tuple(sorted(list(subset) + [candidate]))), weight)

        # Determine the winner through the Schwartz set heuristic
        self.schwartz_set_heuristic()
        self.graph_winner()
        self.winners = set([item for innerlist in self.winners for item in innerlist])
        
    def results(self):
        results = SchulzeMethod.results(self)
        return results
    
    def __generate_vote_management_graph__(self):
        self.vote_management_graph = digraph()
        self.vote_management_graph.add_nodes(self.completed_patterns)
        self.vote_management_graph.del_node(tuple([3]*self.required_winners))
        self.pattern_nodes = self.vote_management_graph.nodes()
        self.vote_management_graph.add_nodes(["source","sink"])
        for pattern_node in self.pattern_nodes:
            self.vote_management_graph.add_edge(("source", pattern_node))
        for i in range(self.required_winners):
            self.vote_management_graph.add_node(i)
        for pattern_node in self.pattern_nodes:
            for i in range(self.required_winners):
                if pattern_node[i] == 1:
                    self.vote_management_graph.add_edge((pattern_node, i))
        for i in range(self.required_winners):        
            self.vote_management_graph.add_edge((i, "sink"))
    
    def __generate_completion_patterns__(self):
        self.completion_patterns = []
        for i in range(0,self.required_winners):
            for j in range(0, i+1):
                for pattern in self.__unique_permutations__([2]*(self.required_winners-i)+[1]*(j)+[3]*(i-j)):
                    self.completion_patterns.append(tuple(pattern))
        
    def __generate_completed_patterns__(self):
        self.completed_patterns = []
        for i in range(0,self.required_winners + 1):
            for pattern in self.__unique_permutations__([1]*(self.required_winners-i)+[3]*(i)):
                self.completed_patterns.append(tuple(pattern))
    
    def __unique_permutations__(self, xs):
        if len(xs)<2:
            yield xs
        else:
            h = []
            for x in xs:
                h.append(x)
                if x in h[:-1]:
                    continue
                ts = xs[:]; ts.remove(x)
                for ps in self.__unique_permutations__(ts):
                    yield [x]+ps
    
    def __proportional_completion__(self, candidate, other_candidates):
        profile = dict(zip(self.completed_patterns, [0]*len(self.completed_patterns)))
        
        # Obtain an initial tally from the ballots
        for ballot in self.ballots:
            pattern = []
            for other_candidate in other_candidates:
                if ballot["ballot"][candidate] < ballot["ballot"][other_candidate]:
                    pattern.append(1)
                elif ballot["ballot"][candidate] == ballot["ballot"][other_candidate]:
                    pattern.append(2)
                else:
                    pattern.append(3)
            pattern = tuple(pattern)
            if pattern not in profile:
                profile[pattern] = 0.0
            profile[pattern] += ballot["count"]

        # Complete each pattern in order
        for pattern in self.completion_patterns:
            if pattern in profile:
                profile = self.__proportional_completion_round__(pattern, profile)

        return profile

    def __proportional_completion_round__(self, completion_pattern, profile):

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
    def __strength_of_vote_management__(self, voter_profile):
        
        # Initialize the graph weights
        for pattern in self.pattern_nodes:
            self.vote_management_graph.set_edge_weight(("source", pattern), voter_profile[pattern])
            for i in range(self.required_winners):
                if pattern[i] == 1:
                    self.vote_management_graph.set_edge_weight((pattern, i), voter_profile[pattern])
        
        # Iterate towards the limit
        r = [(float(sum(voter_profile.values())) - voter_profile[tuple([3]*self.required_winners)]) / self.required_winners]
        while len(r) < 2 or r[-2] - r[-1] > 0.0000000001:
            for i in range(self.required_winners):
                self.vote_management_graph.set_edge_weight((i, "sink"), r[-1])
            max_flow = maximum_flow(self.vote_management_graph, "source", "sink")
            sink_sum = sum(v for k,v in max_flow[0].iteritems() if k[1] == "sink")
            r.append(sink_sum/self.required_winners)
        
        # Return the final max flow
        return round(r[-1],9)