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

import random, math, types

# This class provides methods that most electoral systems make use of.
class VotingSystem(object):
    
    @staticmethod
    def generateTieBreaker(candidates):
        tieBreaker = list(candidates)
        random.shuffle(tieBreaker)
        return tieBreaker

    
    @staticmethod
    def breakTies(tiedObjects, tieBreaker, reverseOrder=False):

        if reverseOrder:
            tieBreaker.reverse()

        if type(list(tiedObjects)[0]) == types.StringType:
            result = VotingSystem.__breakTiesSimple__(tiedObjects, tieBreaker)
        else:
            result = VotingSystem.__breakTiesComplex__(tiedObjects, tieBreaker)

        if reverseOrder:
            tieBreaker.reverse()

        return result


    @staticmethod
    def __breakTiesSimple__(tiedCandidates, tieBreaker):
        for candidate in tieBreaker:
            if candidate in tiedCandidates:
                return candidate


    @staticmethod
    def __breakTiesComplex__(tiedObjects, tieBreaker):
        maxColumns = len(list(tiedObjects)[0])
        column = 0
        while len(tiedObjects) > 1 and column < maxColumns:
            minIndex = min(tieBreaker.index(list(object)[column]) for object in tiedObjects)
            tiedObjects = VotingSystem.matchingKeys(tiedObjects, minIndex)
            column += 1
        return list(tiedObjects)[0]

    
    @staticmethod
    def droopQuota(ballots, seats):
        quota = 0;
        for ballot in ballots:
            quota += ballot["count"]
        return int(math.floor(quota / (seats + 1)) + 1)


    @staticmethod
    def matchingKeys(dict, targetValue):
        return set([key for key, value in dict.iteritems() if value == targetValue])
