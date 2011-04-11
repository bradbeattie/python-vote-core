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

from pyvotecore.plurality_at_large import PluralityAtLarge
import unittest

class TestPluralityAtLarge(unittest.TestCase):
	
	# Plurality at Large, no ties
	def test_plurality_at_large_no_ties(self):
		
		# Generate data
		output = PluralityAtLarge([
			{ "count":26, "ballot":["c1", "c2"] },
			{ "count":22, "ballot":["c1", "c3"] },
			{ "count":23, "ballot":["c2", "c3"] }
		], required_winners = 2).as_dict()
		
		# Run tests
		self.assertEqual(output, {
			'candidates': set(['c1','c2','c3']),
			'tallies': {'c3': 45, 'c2': 49, 'c1': 48},
			'winners': set(['c2', 'c1'])
		})

	
	# Plurality at Large, irrelevant ties
	def test_plurality_at_large_irrelevant_ties(self):
		
		# Generate data
		output = PluralityAtLarge([
			{ "count":26, "ballot":["c1", "c2"] },
			{ "count":22, "ballot":["c1", "c3"] },
			{ "count":22, "ballot":["c2", "c3"] },
			{ "count":11, "ballot":["c4", "c5"] }
		], required_winners = 2).as_dict()
		
		# Run tests
		self.assertEqual(output, {
			'candidates': set(['c1','c2','c3', 'c4', 'c5']),
			'tallies': {'c3': 44, 'c2': 48, 'c1': 48, 'c5': 11, 'c4': 11},
			'winners': set(['c2', 'c1'])
		})

	
	# Plurality at Large, irrelevant ties
	def test_plurality_at_large_relevant_ties(self):
		
		# Generate data
		output = PluralityAtLarge([
			{ "count":30, "ballot":["c1", "c2"] },
			{ "count":22, "ballot":["c3", "c1"] },
			{ "count":22, "ballot":["c2", "c3"] },
			{ "count":4, "ballot":["c4", "c1"] },
			{ "count":8, "ballot":["c3", "c4"] },
		], required_winners = 2).as_dict()
		
		# Run tests
		self.assertEqual(output["tallies"], {'c3': 52, 'c2': 52, 'c1': 56, 'c4': 12})
		self.assertEqual(len(output["tie_breaker"]), 4)
		self.assertEqual(output["tied_winners"], set(['c2','c3']))
		self.assert_("c1" in output["winners"] and ("c2" in output["winners"] or "c3" in output["winners"]))
		self.assertEqual(len(output), 5)


if __name__ == "__main__":
	unittest.main()
