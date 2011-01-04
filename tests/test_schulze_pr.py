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

from schulze_pr import SchulzePR
import unittest

class TestSchulzePR(unittest.TestCase):

	# This example was detailed in Markus Schulze's schulze2.pdf (Free Riding
	# and Vote Management under Proportional Representation by the Single
	# Transferable Vote, section 6.2).
	def test_part_2_of_5_example(self):

		# Generate data
		input = [
			{ "count":  6, "ballot":[["a"], ["d"], ["b"], ["c"], ["e"]] },
			{ "count": 12, "ballot":[["a"], ["d"], ["e"], ["c"], ["b"]] },
			{ "count": 72, "ballot":[["a"], ["d"], ["e"], ["b"], ["c"]] },
			{ "count":  6, "ballot":[["a"], ["e"], ["b"], ["d"], ["c"]] },
			{ "count": 30, "ballot":[["b"], ["d"], ["c"], ["e"], ["a"]] },
			{ "count": 48, "ballot":[["b"], ["e"], ["a"], ["d"], ["c"]] },
			{ "count": 24, "ballot":[["b"], ["e"], ["d"], ["c"], ["a"]] },
			{ "count":168, "ballot":[["c"], ["a"], ["e"], ["b"], ["d"]] },
			{ "count":108, "ballot":[["d"], ["b"], ["e"], ["c"], ["a"]] },
			{ "count": 30, "ballot":[["e"], ["a"], ["b"], ["d"], ["c"]] },
		]
		output = SchulzePR(input, notation = "grouping").results()

		# Run tests
		self.assertEqual(output, {
			"candidates": set(["a","b","c","d","e"]),
			"proportional_ranking": ["e","c","a","b","d"],
			'rounds': [
				{'winner': 'e'},
				{'winner': 'c'},
				{'winner': 'a'},
				{'winner': 'b'},
				{'winner': 'd'}
			],
		})

	def test_ties(self):

		# Generate data
		input = [
			{ "count": 1, "ballot":[["a"], ["d"], ["b"], ["c"], ["e"]] },
			{ "count": 1, "ballot":[["d"], ["a"], ["e"], ["c"], ["b"]] },
		]
		output = SchulzePR(input, notation = "grouping").results()

		# Run tests
		self.assertEqual(output["candidates"], set(["a","b","c","d","e"]))
		self.assertEqual(len(output["tie_breaker"]), 5)
		self.assertEqual(output["rounds"][0]["tied_winners"], set(['a','d']))
		self.assertEqual(output["rounds"][2]["tied_winners"], set(['c','b', 'e']))
		self.assertEqual(len(output["rounds"][3]["tied_winners"]), 2)

	def test_happenstance_example(self):

		# Generate data
		input = [
			{ "count":23, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2 }},
			{ "count": 7, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9 }},
			{ "count": 2, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9 }}
		]
		output = SchulzePR(input, required_winners = 2, notation = "ranking").results()

		# Run tests
		self.assertEqual(output, {
			"candidates": set(["A","B","C","D","E","F"]),
			"proportional_ranking": ["B","C"],
			"rounds": [
				{'winner': 'B'},
				{'winner': 'C'}
			],
		})

if __name__ == "__main__":
	unittest.main()
