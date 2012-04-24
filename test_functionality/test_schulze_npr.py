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

from pyvotecore.schulze_npr import SchulzeNPR
import unittest


class TestSchulzeNPR(unittest.TestCase):

    def test_single_voter(self):

        # Generate data
        input = [
            {"count":1, "ballot":{"A":1, "B":2, "C":3, "D":4, "E":5}},
        ]
        output = SchulzeNPR(input, winner_threshold=5, ballot_notation="ranking").as_dict()

        # Run tests
        self.assertEqual(output, {
            'order': ['A', 'B', 'C', 'D', 'E'],
            'candidates': set(['A', 'B', 'C', 'D', 'E']),
            'rounds': [
                {'winner': 'A'},
                {'winner': 'B'},
                {'winner': 'C'},
                {'winner': 'D'},
                {'winner': 'E'}
            ]
        })

    def test_nonproportionality(self):

        # Generate data
        input = [
            {"count":2, "ballot":{"A":1, "B":2, "C":3, "D":4, "E":5}},
            {"count":1, "ballot":{"A":5, "B":4, "C":3, "D":2, "E":1}},
        ]
        output = SchulzeNPR(input, winner_threshold=5, ballot_notation="ranking").as_dict()

        # Run tests
        self.assertEqual(output, {
            'order': ['A', 'B', 'C', 'D', 'E'],
            'candidates': set(['A', 'B', 'C', 'D', 'E']),
            'rounds': [
                {'winner': 'A'},
                {'winner': 'B'},
                {'winner': 'C'},
                {'winner': 'D'},
                {'winner': 'E'}
            ]
        })


if __name__ == "__main__":
    unittest.main()
