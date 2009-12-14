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