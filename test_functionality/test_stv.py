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

from pyvotecore.stv import STV
import unittest


class TestSTV(unittest.TestCase):

    # STV, no rounds
    def test_stv_landslide(self):

        # Generate data
        input = [
            {"count": 56, "ballot": ["c1", "c2", "c3"]},
            {"count": 40, "ballot": ["c2", "c3", "c1"]},
            {"count": 20, "ballot": ["c3", "c1", "c2"]}
        ]
        output = STV(input, required_winners=2).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3']),
            'quota': 39,
            'rounds': [{
                'tallies': {'c3': 20.0, 'c2': 40.0, 'c1': 56.0},
                'winners': set(['c2', 'c1'])
            }],
            'winners': set(['c2', 'c1'])
        })

    # STV, no rounds
    def test_stv_everyone_wins(self):

        # Generate data
        input = [
            {"count": 56, "ballot": ["c1", "c2", "c3"]},
            {"count": 40, "ballot": ["c2", "c3", "c1"]},
            {"count": 20, "ballot": ["c3", "c1", "c2"]}
        ]
        output = STV(input, required_winners=3).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3']),
            'quota': 30,
            'rounds': [],
            'remaining_candidates': set(['c1', 'c2', 'c3']),
            'winners': set(['c1', 'c2', 'c3'])
        })

    # STV, example from Wikipedia
    # http://en.wikipedia.org/wiki/Single_transferable_vote#An_example
    def test_stv_wiki_example(self):

        # Generate data
        input = [
            {"count": 4, "ballot": ["orange"]},
            {"count": 2, "ballot": ["pear", "orange"]},
            {"count": 8, "ballot": ["chocolate", "strawberry"]},
            {"count": 4, "ballot": ["chocolate", "sweets"]},
            {"count": 1, "ballot": ["strawberry"]},
            {"count": 1, "ballot": ["sweets"]}
        ]
        output = STV(input, required_winners=3).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['orange', 'pear', 'chocolate', 'strawberry', 'sweets']),
            'quota': 6,
            'rounds': [
                {'tallies': {'orange': 4.0, 'strawberry': 1.0, 'pear': 2.0, 'sweets': 1.0, 'chocolate': 12.0}, 'winners': set(['chocolate'])},
                {'tallies': {'orange': 4.0, 'strawberry': 5.0, 'pear': 2.0, 'sweets': 3.0}, 'loser': 'pear'},
                {'tallies': {'orange': 6.0, 'strawberry': 5.0, 'sweets': 3.0}, 'winners': set(['orange'])},
                {'tallies': {'strawberry': 5.0, 'sweets': 3.0}, 'loser': 'sweets'}
            ],
            'remaining_candidates': set(['strawberry']),
            'winners': set(['orange', 'strawberry', 'chocolate'])
        })

    # STV, no rounds
    def test_stv_single_ballot(self):

        # Generate data
        input = [
            {"count": 1, "ballot": ["c1", "c2", "c3", "c4"]},
        ]
        output = STV(input, required_winners=3).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3', 'c4']),
            'quota': 1,
            'rounds': [
                {'tallies': {'c1': 1.0}, 'winners': set(['c1'])},
                {'note': 'reset', 'tallies': {'c2': 1.0}, 'winners': set(['c2'])},
                {'note': 'reset', 'tallies': {'c3': 1.0}, 'winners': set(['c3'])}
            ],
            'winners': set(['c1', 'c2', 'c3'])
        })

    # STV, no rounds
    def test_stv_fewer_voters_than_winners(self):

        # Generate data
        input = [
            {"count": 1, "ballot": ["c1", "c3", "c4"]},
            {"count": 1, "ballot": ["c2", "c3", "c4"]},
        ]
        output = STV(input, required_winners=3).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c1', 'c2', 'c3', 'c4']),
            'quota': 1,
            'rounds': [
                {'tallies': {'c2': 1.0, 'c1': 1.0}, 'winners': set(['c2', 'c1'])},
                {'note': 'reset', 'tallies': {'c3': 2.0}, 'winners': set(['c3'])}
            ],
            'winners': set(['c1', 'c2', 'c3'])
        })

    # STV, Ian Jacobs use-case
    def test_stv_ian_jacobs(self):

        # Generate data
        input = [
            {"count": 1, "ballot": ["AB", "EF", "BC"]},
            {"count": 1, "ballot": ["AB", "KL", "EF", "HI"]},
            {"count": 1, "ballot": ["EF", "AB", "QR"]},
            {"count": 1, "ballot": ["KL", "AB", "BC", "ST", "EF", "QR"]},
            {"count": 1, "ballot": ["ST", "AB", "BC", "QR", "EF", "KL"]},
            {"count": 1, "ballot": ["QR", "BC", "EF"]},
            {"count": 1, "ballot": ["BC", "QR", "AB", "HI"]},
            {"count": 1, "ballot": ["BC", "AB", "ST", "QR", "KL", "EF", "HI"]},
            {"count": 1, "ballot": ["QR", "EF", "AB", "BC", "ST", "KL"]},
            {"count": 1, "ballot": ["KL", "AB", "EF", "QR", "ST", "BC", "HI"]},
            {"count": 1, "ballot": ["AB", "ST", "EF", "KL", "BC", "QR"]},
            {"count": 1, "ballot": ["QR", "ST", "KL", "AB", "BC", "EF", "HI"]},
            {"count": 1, "ballot": ["BC", "QR", "KL"]},
        ]
        output = STV(input, required_winners=3).as_dict()

        # Run tests
        self.assertEqual(output["winners"], set(["AB", "BC", "QR"]))


if __name__ == "__main__":
    unittest.main()
