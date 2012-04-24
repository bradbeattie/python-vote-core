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

import random
import types
from copy import copy

# This class provides tie breaking methods


class TieBreaker(object):

    #
    def __init__(self, candidate_range):
        self.ties_broken = False
        self.random_ordering = list(candidate_range)
        if type(candidate_range) != types.ListType:
            random.shuffle(self.random_ordering)

    #
    def break_ties(self, tied_candidates, reverse=False):
        self.ties_broken = True
        random_ordering = copy(self.random_ordering)
        if reverse:
            random_ordering.reverse()
        if getattr(list(tied_candidates)[0], '__iter__', False):
            result = self.break_complex_ties(tied_candidates, random_ordering)
        else:
            result = self.break_simple_ties(tied_candidates, random_ordering)
        return result

    #
    @staticmethod
    def break_simple_ties(tied_candidates, random_ordering):
        for candidate in random_ordering:
            if candidate in tied_candidates:
                return candidate

    #
    @staticmethod
    def break_complex_ties(tied_candidates, random_ordering):
        max_columns = len(list(tied_candidates)[0])
        column = 0
        while len(tied_candidates) > 1 and column < max_columns:
            min_index = min(random_ordering.index(list(candidate)[column]) for candidate in tied_candidates)
            tied_candidates = set([candidate for candidate in tied_candidates if candidate[column] == random_ordering[min_index]])
            column += 1
        return list(tied_candidates)[0]

    #
    def as_list(self):
        return self.random_ordering

    #
    def __str__(self):
        return "[%s]" % ">".join(self.random_ordering)
