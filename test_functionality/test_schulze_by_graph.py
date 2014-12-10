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

from pyvotecore.schulze_by_graph import SchulzeMethodByGraph, SchulzeNPRByGraph
import unittest


class TestSchulzeMethodByGraph(unittest.TestCase):

    def test_simple_example(self):

        # Generate data
        input = {
            ('a', 'b'): 4,
            ('b', 'a'): 3,
            ('a', 'c'): 4,
            ('c', 'a'): 3,
            ('b', 'c'): 4,
            ('c', 'b'): 3,
        }
        output = SchulzeMethodByGraph(input).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['a', 'b', 'c']),
            'pairs': input,
            'strong_pairs': {
                ('a', 'b'): 4,
                ('a', 'c'): 4,
                ('b', 'c'): 4,
            },
            'winner': 'a',
        })


class TestSchulzeNPRByGraph(unittest.TestCase):

    def test_simple_example(self):

        # Generate data
        input = {
            ('a', 'b'): 8,
            ('b', 'a'): 3,
            ('a', 'c'): 3,
            ('c', 'a'): 4,
            ('b', 'c'): 6,
            ('c', 'b'): 3,
        }
        output = SchulzeNPRByGraph(input, winner_threshold=3).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['a', 'b', 'c']),
            'rounds': [{'winner': 'a'}, {'winner': 'b'}, {'winner': 'c'}],
            'order': ['a', 'b', 'c']
        })

    def test_complex_example(self):

        # Generate data
        input = {
            ('a', 'b'): 4,
            ('b', 'a'): 3,
            ('a', 'c'): 4,
            ('c', 'a'): 3,
            ('b', 'c'): 4,
            ('c', 'b'): 3,
            ('a', 'd'): 4,
            ('d', 'a'): 4,
            ('b', 'd'): 4,
            ('d', 'b'): 4,
            ('c', 'd'): 4,
            ('d', 'c'): 4

        }
        output = SchulzeNPRByGraph(input, winner_threshold=3,
                                   tie_breaker=['a', 'd', 'c', 'b']).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['a', 'b', 'c', 'd']),
            'tie_breaker': ['a', 'd', 'c', 'b'],
            'rounds': [
                {'winner': 'a', 'tied_winners': set(['a', 'd'])},
                {'winner': 'd', 'tied_winners': set(['b', 'd'])},
                {'winner': 'b'},
            ],
            'order': ['a', 'd', 'b'],
        })

if __name__ == "__main__":
    unittest.main()
