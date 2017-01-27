from __future__ import division
from abstract_classes import SingleWinnerVotingSystem

class Range(SingleWinnerVotingSystem):

    def __init__(self, ballots):
        super(Range, self).__init__(ballots)

    def calculate_results(self):
        candidates = {}
        for ballot in self.ballots:
            for candidate, score in ballot["ballot"].iteritems():
                if candidate not in candidates:
                    candidates[candidate] = CandidateResult(candidate)
                candidates[candidate].sum_score += score * ballot["count"]
                candidates[candidate].votes += ballot["count"]
        self.candidates = set(candidates.keys())
        self.results = sorted(candidates.values(), key=lambda cr: cr.avg_score, reverse=True)
        
        top_sum = sorted(candidates.values(), key=lambda cr: cr.sum_score, reverse=True)[0].sum_score
        top_avg = 0
        self.quorum = top_sum / 2
        tied_results = []
        for result in self.results:
            if result.sum_score >= self.quorum and result.avg_score >= top_avg:
                top_avg = result.avg_score
                tied_results.append(result)

        if len(tied_results) == 1:
            self.winner = tied_results[0].name
        else:
            self.winner = self.break_ties([result.name for result in tied_results])

    def as_dict(self):
        data = super(Range, self).as_dict()
        data["results"] = [str(result) for result in self.results]
        data["quorum"] = self.quorum
        return data

    def break_ties(self, tied_candidates):
        points = {}
        for candidate in tied_candidates:
            points[candidate] = 0
        for ballot in self.ballots:
            personal_tied_sum = 0
            for candidate, score in ballot["ballot"].iteritems():
                if candidate in tied_candidates:
                    personal_tied_sum += score
            personal_tied_avg = personal_tied_sum / len(tied_candidates)
            for candidate, score in ballot["ballot"].iteritems():
                if candidate in tied_candidates:
                    if score > personal_tied_avg:
                        points[candidate] += ballot["count"]
        return sorted(points.items(), key=lambda p: p[1], reverse=True)[0][0]

class CandidateResult(object):

    def __init__(self, name, sum_score=0, votes=0):
        self.name, self.sum_score, self.votes = name, sum_score, votes

    @property
    def avg_score(self):
        return self.sum_score / self.votes

    def __str__(self):
        return "{}: {} votes with a total score of {} and an average score of {}.".format(self.name, self.votes, self.sum_score, self.avg_score)

# if __name__ == "__main__":
#     ballots = [
#     {"count": 1, "ballot": {"Gary Johnson": 86, "Fred Karger": 78, "Jill Stein": 77, "Barack Obama": 64, "Ron Paul": 56, "Mitt Romney": 33}}, 
#     {"count": 1, "ballot": {"Barack Obama": 100, "Mitt Romney": 0, "Gary Johnson": 0}}, 
#     {"count": 1, "ballot": {"Mitt Romney": 100, "Barack Obama": 0, "Gary Johnson": 0}},
#     {"count": 1, "ballot": {"Mitt Romney": 0, "Barack Obama": 0, "Ron Paul": 100, "Gary Johnson": 80}}
#     ]
#     print Range(ballots).as_dict()