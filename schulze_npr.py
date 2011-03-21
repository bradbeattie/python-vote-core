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

from schulze_method import SchulzeMethod
from pygraph.algorithms.accessibility import accessibility, mutual_accessibility

# This class implements the an iterated Schulze Method that produces a
# non-proportional ordering.
class SchulzeNPR(SchulzeMethod):

	def __init__(self, ballots, required_winners = None, notation = None):
		self.required_winners = required_winners
		SchulzeMethod.__init__(self, ballots, notation)
		if len(self.candidates) == self.required_winners: self.calculate_results()

	def results(self):
		results = SchulzeMethod.results(self)
		results["nonproportional_ranking"] = self.nonproportional_ranking
		results["rounds"] = self.rounds
		return results

	def calculate_results(self):
		print "CALCULATE RESULTS"

		original_candidates = self.candidates.copy()
		self.nonproportional_ranking = []
		self.rounds = []

		if self.required_winners == None:
			required_winners = len(self.candidates)
		else:
			required_winners = min(len(self.candidates), self.required_winners + 1)

		for self.required_winners in range(1, required_winners):
			
			SchulzeMethod.calculate_results(self)

			# Extract the winner and adjust the remaining candidates list
			self.nonproportional_ranking.append(list(self.winners)[0])
			round = {"winner": list(self.winners)[0]}
			if hasattr(self, 'tied_winners') and len(self.tied_winners) > 0:
				round["tied_winners"] = self.tied_winners
				del self.tied_winners 
			self.rounds.append(round)
			self.candidates -= self.winners

		# Attach the last candidate as the sole winner if necessary
		if required_winners == len(original_candidates):
			self.rounds.append({"winner": list(self.candidates)[0]})
			self.nonproportional_ranking.append(list(self.candidates)[0])
			
		self.candidates = original_candidates
			
		# Remove attributes that only pertain to individual rounds
		del self.winners
		if hasattr(self, 'tied_winners'):
			del self.tied_winners
		if hasattr(self, 'actions'):
			del self.actions
		if hasattr(self, 'strong_pairs'):
			del self.strong_pairs
		if hasattr(self, 'pairs'):
			del self.pairs