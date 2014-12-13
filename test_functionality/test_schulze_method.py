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

from pyvotecore.schulze_method import SchulzeMethod
import unittest


class TestSchulzeMethod(unittest.TestCase):

    # Schulze Method, example from Wikipedia
    # http://en.wikipedia.org/wiki/Schulze_method#The_Schwartz_set_heuristic
    def test_wiki_example(self):

        # Generate data
        input = [
            {"count": 3, "ballot": [["A"], ["C"], ["D"], ["B"]]},
            {"count": 9, "ballot": [["B"], ["A"], ["C"], ["D"]]},
            {"count": 8, "ballot": [["C"], ["D"], ["A"], ["B"]]},
            {"count": 5, "ballot": [["D"], ["A"], ["B"], ["C"]]},
            {"count": 5, "ballot": [["D"], ["B"], ["C"], ["A"]]}
        ]
        output = SchulzeMethod(input, ballot_notation=SchulzeMethod.BALLOT_NOTATION_GROUPING).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['A', 'C', 'B', 'D']),
            'pairs': {
                ('A', 'B'): 16,
                ('A', 'C'): 17,
                ('A', 'D'): 12,
                ('B', 'A'): 14,
                ('B', 'C'): 19,
                ('B', 'D'): 9,
                ('C', 'A'): 13,
                ('C', 'B'): 11,
                ('C', 'D'): 20,
                ('D', 'A'): 18,
                ('D', 'B'): 21,
                ('D', 'C'): 10
            },
            'strong_pairs': {
                ('D', 'B'): 21,
                ('C', 'D'): 20,
                ('B', 'C'): 19,
                ('D', 'A'): 18,
                ('A', 'C'): 17,
                ('A', 'B'): 16,
            },
            'actions': [
                {'edges': set([('A', 'B')])},
                {'edges': set([('A', 'C')])},
                {'nodes': set(['A'])},
                {'edges': set([('B', 'C')])},
                {'nodes': set(['B', 'D'])}
            ],
            'winner': 'C'
        })

    # http://en.wikipedia.org/wiki/Schulze_method#Example
    def test_wiki_example2(self):

        # Generate data
        input = [
            {"count": 5, "ballot": [["A"], ["C"], ["B"], ["E"], ["D"]]},
            {"count": 5, "ballot": [["A"], ["D"], ["E"], ["C"], ["B"]]},
            {"count": 8, "ballot": [["B"], ["E"], ["D"], ["A"], ["C"]]},
            {"count": 3, "ballot": [["C"], ["A"], ["B"], ["E"], ["D"]]},
            {"count": 7, "ballot": [["C"], ["A"], ["E"], ["B"], ["D"]]},
            {"count": 2, "ballot": [["C"], ["B"], ["A"], ["D"], ["E"]]},
            {"count": 7, "ballot": [["D"], ["C"], ["E"], ["B"], ["A"]]},
            {"count": 8, "ballot": [["E"], ["B"], ["A"], ["D"], ["C"]]}
        ]
        output = SchulzeMethod(input, ballot_notation=SchulzeMethod.BALLOT_NOTATION_GROUPING).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['A', 'C', 'B', 'E', 'D']),
            'pairs': {
                ('A', 'B'): 20,
                ('A', 'C'): 26,
                ('A', 'D'): 30,
                ('A', 'E'): 22,
                ('B', 'A'): 25,
                ('B', 'C'): 16,
                ('B', 'D'): 33,
                ('B', 'E'): 18,
                ('C', 'A'): 19,
                ('C', 'B'): 29,
                ('C', 'D'): 17,
                ('C', 'E'): 24,
                ('D', 'A'): 15,
                ('D', 'B'): 12,
                ('D', 'C'): 28,
                ('D', 'E'): 14,
                ('E', 'A'): 23,
                ('E', 'B'): 27,
                ('E', 'C'): 21,
                ('E', 'D'): 31
            },
            'strong_pairs': {
                ('B', 'D'): 33,
                ('E', 'D'): 31,
                ('A', 'D'): 30,
                ('C', 'B'): 29,
                ('D', 'C'): 28,
                ('E', 'B'): 27,
                ('A', 'C'): 26,
                ('B', 'A'): 25,
                ('C', 'E'): 24,
                ('E', 'A'): 23
            },
            'actions': [
                {'edges': set([('E', 'A')])},
                {'edges': set([('C', 'E')])},
                {'nodes': set(['A', 'C', 'B', 'D'])}
            ],
            'winner': 'E'
        })

    def test_tiebreaker_bug(self):

        # Generate data
        input = [
            {"count": 1, "ballot": [["A"], ["B", "C"]]},
            {"count": 1, "ballot": [["B"], ["A"], ["C"]]},
        ]
        output = SchulzeMethod(input, ballot_notation=SchulzeMethod.BALLOT_NOTATION_GROUPING).as_dict()

        # Run tests
        self.assertEqual(output['candidates'], set(['A', 'B', 'C']))
        self.assertEqual(output['pairs'], {
            ('A', 'B'): 1,
            ('A', 'C'): 2,
            ('B', 'A'): 1,
            ('B', 'C'): 1,
            ('C', 'A'): 0,
            ('C', 'B'): 0,
        })
        self.assertEqual(output['strong_pairs'], {
            ('A', 'C'): 2,
            ('B', 'C'): 1,
        })
        self.assertEqual(output['tied_winners'], set(['A', 'B']))


if __name__ == "__main__":
    unittest.main()
