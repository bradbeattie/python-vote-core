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
from schulze_stv import SchulzeSTV
from pygraph.classes.digraph import digraph

class SchulzePR(SchulzeSTV):
    
    def __init__(self, ballots, required_winners = None, notation = None):
        SchulzeSTV.__init__(self, ballots, required_winners, notation)
        
    def results(self):
        results = SchulzeSTV.results(self)
        results["proportional_ranking"] = self.proportional_ranking
        results["rounds"] = self.rounds
        return results
        
    def calculate_results(self):
        
        remaining_candidates = self.candidates.copy()
        self.proportional_ranking = []
        self.rounds = []
        
        if self.required_winners == None:
            required_winners = len(self.candidates)
        else:
            required_winners = min(len(self.candidates), self.required_winners + 1)

        for self.required_winners in range(1, required_winners):
            
            # Generate the list of patterns we need to complete
            self.__generate_completion_patterns__()
            self.__generate_completed_patterns__()
            self.__generate_vote_management_graph__()
                
            # Generate the edges between nodes
            self.graph = digraph()
            self.graph.add_nodes(remaining_candidates)
            self.winners = set([])
            self.tied_winners = set([])
            
            # Generate the edges between nodes
            for candidate_from in remaining_candidates:
                other_candidates = sorted(list(remaining_candidates - set([candidate_from])))
                for candidate_to in other_candidates:
                    completed = self.__proportional_completion__(candidate_from, set([candidate_to]) | set(self.proportional_ranking))
                    weight = self.__strength_of_vote_management__(completed)
                    if weight > 0:
                        self.graph.add_edge((candidate_to, candidate_from), weight)
            
            # Determine the round winner through the Schwartz set heuristic
            self.schwartz_set_heuristic()
            
            # Extract the winner and adjust the remaining candidates list
            self.proportional_ranking.append(list(self.winners)[0])
            round = {"winner": list(self.winners)[0]}
            if len(self.tied_winners) > 0:
                round["tied_winners"] = self.tied_winners
            self.rounds.append(round)
            remaining_candidates -= self.winners
        
        # Attach the last candidate as the sole winner if necessary
        if required_winners == len(self.candidates):
            self.rounds.append({"winner": list(remaining_candidates)[0]})
            self.proportional_ranking.append(list(remaining_candidates)[0])
        
        # Remove attributes that only pertain to individual rounds
        if hasattr(self, 'tied_winners'):
            del self.tied_winners
        del self.winners
        del self.actions