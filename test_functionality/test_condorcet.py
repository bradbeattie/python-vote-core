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


class TestCondorcet(unittest.TestCase):

    def test_grouping_format(self):

        # Generate data
        input = [
            {"count": 12, "ballot": [["Andrea"], ["Brad"], ["Carter"]]},
            {"count": 26, "ballot": [["Andrea"], ["Carter"], ["Brad"]]},
            {"count": 12, "ballot": [["Andrea"], ["Carter"], ["Brad"]]},
            {"count": 13, "ballot": [["Carter"], ["Andrea"], ["Brad"]]},
            {"count": 27, "ballot": [["Brad"]]},
        ]
        output = SchulzeMethod(input, ballot_notation="grouping").as_dict()

        # Run tests
        self.assertEqual(output, {
            "candidates": set(['Carter', 'Brad', 'Andrea']),
            "pairs": {
                ('Andrea', 'Brad'): 63,
                ('Brad', 'Carter'): 39,
                ('Carter', 'Andrea'): 13,
                ('Andrea', 'Carter'): 50,
                ('Brad', 'Andrea'): 27,
                ('Carter', 'Brad'): 51
            },
            "strong_pairs": {
                ('Andrea', 'Brad'): 63,
                ('Carter', 'Brad'): 51,
                ('Andrea', 'Carter'): 50
            },
            "winner": 'Andrea'
        })

    def test_ranking_format(self):

        # Generate data
        input = [
            {"count": 12, "ballot": {"Andrea": 1, "Brad": 2, "Carter": 3}},
            {"count": 26, "ballot": {"Andrea": 1, "Carter": 2, "Brad": 3}},
            {"count": 12, "ballot": {"Andrea": 1, "Carter": 2, "Brad": 3}},
            {"count": 13, "ballot": {"Carter": 1, "Andrea": 2, "Brad": 3}},
            {"count": 27, "ballot": {"Brad": 1}}
        ]
        output = SchulzeMethod(input, ballot_notation="ranking").as_dict()

        # Run tests
        self.assertEqual(output, {
            "candidates": set(['Carter', 'Brad', 'Andrea']),
            "pairs": {
                ('Andrea', 'Brad'): 63,
                ('Brad', 'Carter'): 39,
                ('Carter', 'Andrea'): 13,
                ('Andrea', 'Carter'): 50,
                ('Brad', 'Andrea'): 27,
                ('Carter', 'Brad'): 51
            },
            "strong_pairs": {
                ('Andrea', 'Brad'): 63,
                ('Carter', 'Brad'): 51,
                ('Andrea', 'Carter'): 50
            },
            "winner": 'Andrea'
        })

    def test_rating_format(self):

        # Generate data
        input = [
            {"count": 12, "ballot": {"Andrea": 10, "Brad": 5, "Carter": 3}},
            {"count": 26, "ballot": {"Andrea": 10, "Carter": 5, "Brad": 3}},
            {"count": 12, "ballot": {"Andrea": 10, "Carter": 5, "Brad": 3}},
            {"count": 13, "ballot": {"Carter": 10, "Andrea": 5, "Brad": 3}},
            {"count": 27, "ballot": {"Brad": 10}}
        ]
        output = SchulzeMethod(input, ballot_notation="rating").as_dict()

        # Run tests
        self.assertEqual(output, {
            "candidates": set(['Carter', 'Brad', 'Andrea']),
            "pairs": {
                ('Andrea', 'Brad'): 63,
                ('Brad', 'Carter'): 39,
                ('Carter', 'Andrea'): 13,
                ('Andrea', 'Carter'): 50,
                ('Brad', 'Andrea'): 27,
                ('Carter', 'Brad'): 51
            },
            "strong_pairs": {
                ('Andrea', 'Brad'): 63,
                ('Carter', 'Brad'): 51,
                ('Andrea', 'Carter'): 50
            },
            "winner": 'Andrea'
        })

if __name__ == "__main__":
    unittest.main()
