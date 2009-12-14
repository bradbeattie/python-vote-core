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

#An example of a class
import random
class VotingSystem:
    
    @staticmethod
    def generateTieBreaker(candidates):
        tieBreaker = list(candidates)
        random.shuffle(tieBreaker)
        return tieBreaker
    
    @staticmethod
    def breakWinnerTie(tiedCandidates, tieBreaker):
        for candidate in tieBreaker:
            if candidate in tiedCandidates:
                return candidate

    @staticmethod
    def breakLoserTie(tiedCandidates, tieBreaker):
        tieBreaker.reverse()
        candidate = VotingSystem.breakWinnerTie(tiedCandidates, tieBreaker)
        tieBreaker.reverse() # Is this second reversal necessary?
        return candidate
            
    @staticmethod
    def breakStrongestPairTie(tiedPairs, tieBreaker):
        for candidate in tieBreaker:
            for pair in tiedPairs:
                if pair[0] == candidate:
                    return pair

    @staticmethod
    def breakWeakestPairTie(tiedPairs, tieBreaker):
        tieBreaker.reverse()
        pair = VotingSystem.breakStrongestPairTie(tiedPairs, tieBreaker)
        tieBreaker.reverse() # Is this second reversal necessary?
        return pair