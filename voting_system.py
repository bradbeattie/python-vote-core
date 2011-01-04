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

# This class provides methods that most electoral systems make use of.
class VotingSystem(object):

	required_winners = 1

	def __init__(self):
		self.tie_breaker = TieBreaker(self.candidates)
		if len(self.candidates) < self.required_winners:
			raise Exception("Insufficient candidates to meet produce sufficient winners")
		elif len(self.candidates) == self.required_winners:
			self.winners = self.candidates
		else:
			self.calculate_results()

	def calculate_results(self):
		pass

	def results(self):
		results = {
			"candidates": self.candidates
		}
		if hasattr(self, 'winners'):
			results["winners"] = self.winners
		if hasattr(self.tie_breaker, 'random_ordering'):
			results["tie_breaker"] = self.tie_breaker.random_ordering
		return results

	def break_ties(self, tied_objects, reverse_order=False):
		return self.tie_breaker.break_ties(tied_objects, reverse_order)

	@staticmethod
	def matching_keys(dict, target_value):
		return set([
			key
			for key, value in dict.iteritems()
			if value == target_value
		])
