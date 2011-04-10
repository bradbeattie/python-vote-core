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

from pyvotecore.irv import IRV
import unittest

class TestInstantRunoff(unittest.TestCase):
	
	# IRV, no ties
	def test_irv_no_ties(self):
		
		# Generate data
		input = [
			{ "count":26, "ballot":["c1", "c2", "c3"] },
			{ "count":20, "ballot":["c2", "c3", "c1"] },
			{ "count":23, "ballot":["c3", "c1", "c2"] }
		]
		output = IRV(input).as_dict()
		
		# Run tests
		self.assertEqual(output, {
			'candidates': set(['c1','c2','c3']),
			'quota': 35,
			'winner': 'c3',
			'rounds': [
				{'tallies': {'c3': 23.0, 'c2': 20.0, 'c1': 26.0}, 'loser': 'c2'},
				{'tallies': {'c3': 43.0, 'c1': 26.0}, 'winner': 'c3'}
			]
		})

	
	# IRV, ties
	def test_irv_ties(self):
		
		# Generate data
		input = [
			{ "count":26, "ballot":["c1", "c2", "c3"] },
			{ "count":20, "ballot":["c2", "c3", "c1"] },
			{ "count":20, "ballot":["c3", "c1", "c2"] }
		]
		output = IRV(input).as_dict()
		
		# Run tests
		self.assertEqual(output["quota"], 34)
		self.assertEqual(len(output["rounds"]), 2)
		self.assertEqual(len(output["rounds"][0]), 3)
		self.assertEqual(output["rounds"][0]["tallies"], {'c1': 26, 'c2': 20, 'c3': 20})
		self.assertEqual(output["rounds"][0]["tied_losers"], set(['c2','c3']))
		self.assert_(output["rounds"][0]["loser"] in output["rounds"][0]["tied_losers"])
		self.assertEqual(len(output["rounds"][1]["tallies"]), 2)
		self.assert_("winner" in output["rounds"][1])
		self.assertEqual(len(output["tie_breaker"]), 3)

	
	# IRV, no rounds
	def test_irv_landslide(self):
		
		# Generate data
		input = [
			{ "count":56, "ballot":["c1", "c2", "c3"] },
			{ "count":20, "ballot":["c2", "c3", "c1"] },
			{ "count":20, "ballot":["c3", "c1", "c2"] }
		]
		output = IRV(input).as_dict()
		
		# Run tests
		self.assertEqual(output, {
			'candidates': set(['c1','c2','c3']),
			'quota': 49,
			'winner': 'c1',
			'rounds': [
				{'tallies': {'c3': 20.0, 'c2': 20.0, 'c1': 56.0}, 'winner': 'c1'}
			]
		})

if __name__ == "__main__":
	unittest.main()
