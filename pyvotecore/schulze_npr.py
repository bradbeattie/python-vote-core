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

from abstract_classes import AbstractOrderingVotingSystem
from schulze_helper import SchulzeHelper
from schulze_method import SchulzeMethod

#
class SchulzeNPR(AbstractOrderingVotingSystem, SchulzeHelper):
	
	def __init__(self, ballots, winner_threshold = None, tie_breaker = None, ballot_notation = None):
		self.standardize_ballots(ballots, ballot_notation)
		super(SchulzeNPR, self).__init__(self.ballots,
			single_winner_class = SchulzeMethod,
			winner_threshold = winner_threshold,
			tie_breaker = tie_breaker,
		)
	
	@staticmethod
	def ballots_without_candidate(ballots, candidate):
		for ballot in ballots:
			if candidate in ballot['ballot']:
				del ballot['ballot'][candidate]
		return ballots
