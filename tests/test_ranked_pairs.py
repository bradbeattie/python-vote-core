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

from ranked_pairs import RankedPairs
import unittest

class TestRankedPairs(unittest.TestCase):
    
    # Ranked Pairs, cycle
    def test_no_cycle(self):
        
        # Generate data
        input = [
            { "count":80, "ballot":[["c1", "c2"], ["c3"]] },
            { "count":50, "ballot":[["c2"], ["c3", "c1"]] },
            { "count":40, "ballot":[["c3"], ["c1"], ["c2"]] }
        ]
        output = RankedPairs.calculate_winner(input)
        
        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c3', 'c2', 'c1']),
            'pairs': {
                ('c1', 'c2'): 40,
                ('c1', 'c3'): 80,
                ('c2', 'c1'): 50,
                ('c2', 'c3'): 130,
                ('c3', 'c1'): 40,
                ('c3', 'c2'): 40
            },
            'strong_pairs': {
                ('c2', 'c3'): 130,
                ('c1', 'c3'): 80,
                ('c2', 'c1'): 50
            },
            'winners': set(['c2'])
        })
        

    # Ranked Pairs, cycle
    def test_cycle(self):
        
        # Generate data
        input = [
            { "count":80, "ballot":[["c1"], ["c2"], ["c3"]] },
            { "count":50, "ballot":[["c2"], ["c3"], ["c1"]] },
            { "count":40, "ballot":[["c3"], ["c1"], ["c2"]] }
        ]
        output = RankedPairs.calculate_winner(input)
        
        # Run tests
        self.assertEqual(output, {
            'candidates': set(['c3', 'c2', 'c1']),
            'pairs': {
                ('c1', 'c3'): 80,
                ('c1', 'c2'): 120,
                ('c2', 'c1'): 50,
                ('c2', 'c3'): 130,
                ('c3', 'c1'): 90,
                ('c3', 'c2'): 40
            },
            'strong_pairs': {
                ('c2', 'c3'): 130,
                ('c1', 'c2'): 120,
                ('c3', 'c1'): 90
            },
            'rounds': [
                {'pair': ('c2', 'c3'), 'action': 'added'},
                {'pair': ('c1', 'c2'), 'action': 'added'},
                {'pair': ('c3', 'c1'), 'action': 'skipped'}
            ],
            'winners': set(['c1'])
        })

    # Strongest pairs tie
    def test_tied_pairs(self):
        
        # Generate data
        input = [
            { "count":100, "ballot":[["chocolate"], ["vanilla"]] },
            { "count":100, "ballot":[["vanilla"], ["strawberry"]] },
            { "count":1, "ballot":[["strawberry"], ["chocolate"]] }
        ]
        output = RankedPairs.calculate_winner(input)

        # Run tests
        self.assertEqual(output["pairs"], {
            ('vanilla', 'strawberry'): 200,
            ('strawberry', 'vanilla'): 1,
            ('chocolate', 'vanilla'): 101,
            ('vanilla', 'chocolate'): 100,
            ('strawberry', 'chocolate'): 101,
            ('chocolate', 'strawberry'): 100
        })

        self.assertEqual(output["strong_pairs"], {
            ('chocolate', 'vanilla'): 101,
            ('vanilla', 'strawberry'): 200,
            ('strawberry', 'chocolate'): 101
        })

        self.assertEqual(
            output["rounds"][1]["tied_pairs"],
            set([('chocolate', 'vanilla'), ('strawberry', 'chocolate')])
        )

if __name__ == "__main__":
    unittest.main()
