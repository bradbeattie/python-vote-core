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

from tie_breaker import TieBreaker
from abc import ABCMeta, abstractmethod
from copy import copy, deepcopy
import types

# This class provides methods that most electoral systems make use of.
class VotingSystem(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, tie_breaker = None):
		self.ballots = ballots
		for ballot in self.ballots:
			if "count" not in ballot:
				ballot["count"] = 1
		self.tie_breaker = tie_breaker
		if type(self.tie_breaker) == types.ListType:
			self.tie_breaker = TieBreaker(self.tie_breaker)
		self.calculate_results()
	
	@abstractmethod
	def as_dict(self):
		data = dict()
		data["candidates"] = self.candidates
		if self.tie_breaker and self.tie_breaker.ties_broken:
			data["tie_breaker"] = self.tie_breaker.as_list()
		return data
	
	def break_ties(self, tied_objects, reverse_order = False):
		if self.tie_breaker == None:
			self.tie_breaker = TieBreaker(self.candidates)
		return self.tie_breaker.break_ties(tied_objects, reverse_order)

# Given a set of candidates, return a fixed number of winners
class FixedWinnerVotingSystem(VotingSystem):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, tie_breaker = None):
		super(FixedWinnerVotingSystem, self).__init__(ballots, tie_breaker)
	
	def as_dict(self):
		data = super(FixedWinnerVotingSystem, self).as_dict()
		if hasattr(self, 'tied_winners'):
			data["tied_winners"] = self.tied_winners
		return data

# Given a set of candidates, return a fixed number of winners
class MultipleWinnerVotingSystem(FixedWinnerVotingSystem):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, tie_breaker = None, required_winners = 1):
		self.required_winners = required_winners
		super(MultipleWinnerVotingSystem, self).__init__(ballots, tie_breaker)
	
	def calculate_results(self):
		if self.required_winners == len(self.candidates):
			self.winners = self.candidates
	
	def as_dict(self):
		data = super(MultipleWinnerVotingSystem, self).as_dict()
		data["winners"] = self.winners
		return data

# Given a set of candidates, return a fixed number of winners
class SingleWinnerVotingSystem(FixedWinnerVotingSystem):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, tie_breaker = None):
		super(SingleWinnerVotingSystem, self).__init__(ballots, tie_breaker)
	
	def as_dict(self):
		data = super(SingleWinnerVotingSystem, self).as_dict()
		data["winner"] = self.winner
		return data

# Given a set of candidates, return a fixed number of winners
class AbstractSingleWinnerVotingSystem(SingleWinnerVotingSystem):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, multiple_winner_class, tie_breaker = None):
		self.multiple_winner_class = multiple_winner_class
		super(AbstractSingleWinnerVotingSystem, self).__init__(ballots, tie_breaker = tie_breaker)
	
	def calculate_results(self):
		self.multiple_winner_instance = self.multiple_winner_class(self.ballots, tie_breaker = self.tie_breaker, required_winners = 1)
		self.__dict__.update(self.multiple_winner_instance.__dict__)
		self.winner = list(self.winners)[0]
		del self.winners
	
	def as_dict(self):
		data = super(AbstractSingleWinnerVotingSystem, self).as_dict()
		data.update(self.multiple_winner_instance.as_dict())
		del data["winners"]
		return data

# Given a set of candidates, return an ordering
class OrderingVotingSystem(VotingSystem):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, tie_breaker = None, winner_threshold = None):
		self.winner_threshold = winner_threshold
		super(OrderingVotingSystem, self).__init__(ballots, tie_breaker = tie_breaker)
	
	def as_dict(self):
		data = super(OrderingVotingSystem, self).as_dict()
		data["order"] = self.order
		return data

# Given a single winner system, generate a non-proportional ordering by sequentially removing the winner
class AbstractOrderingVotingSystem(OrderingVotingSystem):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, ballots, single_winner_class, winner_threshold = None, tie_breaker = None):
		self.single_winner_class = single_winner_class
		super(AbstractOrderingVotingSystem, self).__init__(ballots, winner_threshold = winner_threshold, tie_breaker = tie_breaker)
	
	def calculate_results(self):
		self.order = []
		self.rounds = []
		remaining_ballots = deepcopy(self.ballots)
		remaining_candidates = True
		while (remaining_candidates == True or len(remaining_candidates) > 1) and (self.winner_threshold == None or len(self.order) < self.winner_threshold):
			
			# Given the remaining ballots, who should win?
			result = self.single_winner_class(deepcopy(remaining_ballots), tie_breaker = self.tie_breaker)
			
			# Mark the candidate that won
			r = {'winner': result.winner}
			self.order.append(r['winner'])
			
			# Mark any ties that might have occurred
			if hasattr(result, 'tie_breaker'):
				self.tie_breaker = result.tie_breaker
				if hasattr(result, 'tied_winners'):
					r['tied_winners'] = result.tied_winners
			self.rounds.append(r)
			
			# Remove the candidate from the remaining candidates and ballots
			if remaining_candidates == True:
				self.candidates = result.candidates
				remaining_candidates = copy(self.candidates)
			remaining_candidates.remove(result.winner)
			remaining_ballots = self.ballots_without_candidate(result.ballots, result.winner)
		
		# Note the last remaining candidate
		if (self.winner_threshold == None or len(self.order) < self.winner_threshold): 
			r = {'winner': list(remaining_candidates)[0]}
			self.order.append(r['winner'])
			self.rounds.append(r)
	
	def as_dict(self):
		data = super(AbstractOrderingVotingSystem, self).as_dict()
		data["rounds"] = self.rounds
		return data
