from votingSystem import VotingSystem
import math, copy
class InstantRunoffVote(VotingSystem):
    
    @staticmethod
    def calculateWinner(ballots):
        result = {"rounds": []}
        
        # Determine the number of votes necessary to win
        quota = 0;
        for ballot in ballots:
            quota += ballot["count"]
        quota = int(math.floor(quota / 2) + 1);
        result["quota"] = quota
        
        # Collect the list of candidates
        candidates = set()
        for ballot in ballots:
            candidates.add(ballot["ballot"][0])
        
        # Generate tie breaker
        tieBreaker = InstantRunoffVote.generateTieBreaker(candidates)

        # Loop until a candidate has obtained a majority of votes
        tallies = {}
        while len(tallies) == 0 or max(tallies.values()) < quota:
            round = {}
            
            # Elimination step
            if len(tallies) > 0:

                # Determine which candidates have the fewest votes
                fewestVotes = min(tallies.values())
                leastPreferredCandidates = set()
                for candidate in tallies.keys():
                    if tallies[candidate] == fewestVotes:
                        leastPreferredCandidates.add(candidate)
                if len(leastPreferredCandidates) > 1:
                    result["tieBreaker"] = tieBreaker
                    round["tiedLosers"] = leastPreferredCandidates
                    loser = InstantRunoffVote.breakLoserTie(leastPreferredCandidates, tieBreaker)
                    
                else:
                    loser = list(leastPreferredCandidates)[0]
                round["loser"] = loser
                
                # Eliminate references to the lost candidate
                candidates.remove(loser)
                for ballot in ballots:
                    if loser in ballot["ballot"]:
                        ballot["ballot"].remove(loser)
                        
                result["rounds"].append(round)
                round["tallies"] = copy.deepcopy(tallies)
                        
            # Sum up all votes for each candidate
            tallies = dict.fromkeys(candidates, 0)
            for ballot in ballots:
                if len(ballot["ballot"]) > 0:
                    tallies[ballot["ballot"][0]] +=  ballot["count"]
            
        # Append the final winner and return
        result["winners"] = set([max(tallies, key=tallies.get)])
        return result