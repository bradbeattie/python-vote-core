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

from stv import STV 
import unittest

class TestSTV(unittest.TestCase):
    
    # IRV, no ties
    def testIRVNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":23, "ballot":["c3", "c1", "c2"] }
        ]
        output = STV.calculate_winner(input)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 35,
            'winners': set(['c3']),
            'rounds': [
                {'tallies': {'c3': 23.0, 'c2': 20.0, 'c1': 26.0}, 'loser': 'c2'},
                {'tallies': {'c3': 43.0, 'c1': 26.0}, 'winners': set(['c3'])}
            ]
        })
        
    
    # IRV, ties
    def testIRVTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":20, "ballot":["c3", "c1", "c2"] }
        ]
        output = STV.calculate_winner(input)
        
        # Run tests
        self.assertEqual(output["quota"], 34)
        self.assertEqual(len(output["rounds"]), 2)
        self.assertEqual(len(output["rounds"][0]), 3)
        self.assertEqual(output["rounds"][0]["tallies"], {'c1': 26, 'c2': 20, 'c3': 20})
        self.assertEqual(output["rounds"][0]["tied_losers"], set(['c2','c3']))
        self.assert_(output["rounds"][0]["loser"] in output["rounds"][0]["tied_losers"])
        self.assertEqual(len(output["rounds"][1]["tallies"]), 2)
        self.assertEqual(len(output["rounds"][1]["winners"]), 1)
        self.assertEqual(len(output["tie_breaker"]), 3)


    # IRV, no rounds
    def testIRVLandslide(self):
        
        # Generate data
        input = [
            { "count":56, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":20, "ballot":["c3", "c1", "c2"] }
        ]
        output = STV.calculate_winner(input)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 49,
            'winners': set(['c1']),
            'rounds': [{
                'tallies': {'c3': 20.0, 'c2': 20.0, 'c1': 56.0},
                'winners': set(['c1'])
            }]
        })


    # STV, no rounds
    def testSTVLandslide(self):
        
        # Generate data
        input = [
            { "count":56, "ballot":["c1", "c2", "c3"] },
            { "count":40, "ballot":["c2", "c3", "c1"] },
            { "count":20, "ballot":["c3", "c1", "c2"] }
        ]
        output = STV.calculate_winner(input, 2)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 39,
            'rounds': [{
                'tallies': {'c3': 20.0, 'c2': 40.0, 'c1': 56.0},
                'winners': set(['c2', 'c1'])
            }],
            'winners': set(['c2', 'c1'])
        })
        

    # STV, example from Wikipedia
    # http://en.wikipedia.org/wiki/Single_transferable_vote#An_example
    def testSTVWikiExample(self):

        # Generate data
        input = [
            { "count":4, "ballot":["orange"] },
            { "count":2, "ballot":["pear", "orange"] },
            { "count":8, "ballot":["chocolate", "strawberry"] },
            { "count":4, "ballot":["chocolate", "sweets"] },
            { "count":1, "ballot":["strawberry"] },
            { "count":1, "ballot":["sweets"] }
        ]
        output = STV.calculate_winner(input, 3)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 6,
            'rounds': [
                {'tallies': {'orange': 4.0, 'strawberry': 1.0, 'pear': 2.0, 'sweets': 1.0, 'chocolate': 12.0},'winners': set(['chocolate'])},
                {'tallies': {'orange': 4.0, 'strawberry': 5.0, 'pear': 2.0, 'sweets': 3.0}, 'loser': 'pear'},
                {'tallies': {'orange': 6.0, 'strawberry': 5.0, 'sweets': 3.0}, 'winners': set(['orange'])},
                {'tallies': {'strawberry': 5.0, 'sweets': 3.0}, 'loser': 'sweets'}
            ],
            'remaining_candidates': set(['strawberry']),
            'winners': set(['orange', 'strawberry', 'chocolate'])
        })


if __name__ == "__main__":
    unittest.main()
