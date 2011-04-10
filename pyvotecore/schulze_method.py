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

from schulze_helper import SchulzeHelper
from condorcet import CondorcetSystem
from pygraph.algorithms.accessibility import accessibility, mutual_accessibility
from common_functions import matching_keys

# This class implements the Schulze Method (aka the beatpath method)
class SchulzeMethod(CondorcetSystem, SchulzeHelper):
	
	def __init__(self, ballots, tie_breaker = None, ballot_notation = None):
		CondorcetSystem.__init__(self, ballots, tie_breaker = tie_breaker, ballot_notation = ballot_notation)
	
	def as_dict(self):
		data = super(SchulzeMethod, self).as_dict()
		if hasattr(self, 'actions'):
			data["actions"] = self.actions
		return data
