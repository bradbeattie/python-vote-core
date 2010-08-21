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

import random, types

# This class provides methods that most electoral systems make use of.
class VotingSystem(object):

    required_winners = 1
    
    def __init__(self):
        self.calculate_results()
        
    def calculate_results(self):
        pass
        
    def results(self):
        results = {
            "winners": self.winners
        }
        if hasattr(self, 'tie_breaker'):
            results["tie_breaker"] = self.tie_breaker
        return results

    def break_ties(self, tied_objects, reverse_order=False):
        tie_breaker = self.__generate_tie_breaker__()
        if reverse_order:
            tie_breaker.reverse()
        if type(list(tied_objects)[0]) in [types.UnicodeType, types.StringType]:
            result = self.__break_ties_simple__(tied_objects, tie_breaker)
        else:
            result = self.__break_ties_complex__(tied_objects, tie_breaker)
        if reverse_order:
            tie_breaker.reverse() # TODO: Check to see if this is necessary
        return result

    def __break_ties_simple__(self, tied_candidates, tie_breaker):
        for candidate in tie_breaker:
            if candidate in tied_candidates:
                return candidate

    def __generate_tie_breaker__(self):
        if hasattr(self, 'tie_breaker') == False: 
            self.tie_breaker = list(self.candidates)
            random.shuffle(self.tie_breaker)
        return self.tie_breaker

    def __break_ties_complex__(self, tied_objects, tie_breaker):
        max_columns = len(list(tied_objects)[0])
        column = 0
        while len(tied_objects) > 1 and column < max_columns:
            min_index = min(tie_breaker.index(list(object)[column]) for object in tied_objects)
            tied_objects = set([object for object in tied_objects if object[column] == tie_breaker[min_index]])
            column += 1
        return list(tied_objects)[0]

    @staticmethod
    def matching_keys(dict, target_value):
        return set([
            key
            for key, value in dict.iteritems()
            if value == target_value
        ])
