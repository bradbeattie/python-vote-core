
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

from schulze_stv import SchulzeSTV
import unittest

class TestSchulzeSTV(unittest.TestCase):
    
    # This example was detailed in Markus Schulze's schulze2.pdf (Free Riding
    # and Vote Management under Proportional Representation by the Single
    # Transferable Vote, section 5.5). 
    def test_part_2_of_5_example(self):
        
        # Generate data
        input = [
            { "count":60, "ballot":[["a"], ["b"], ["c"], ["d"], ["e"]] },
            { "count":45, "ballot":[["a"], ["c"], ["e"], ["b"], ["d"]] },
            { "count":30, "ballot":[["a"], ["d"], ["b"], ["e"], ["c"]] },
            { "count":15, "ballot":[["a"], ["e"], ["d"], ["c"], ["b"]] },
            { "count":12, "ballot":[["b"], ["a"], ["e"], ["d"], ["c"]] },
            { "count":48, "ballot":[["b"], ["c"], ["d"], ["e"], ["a"]] },
            { "count":39, "ballot":[["b"], ["d"], ["a"], ["c"], ["e"]] },
            { "count":21, "ballot":[["b"], ["e"], ["c"], ["a"], ["d"]] },
            { "count":27, "ballot":[["c"], ["a"], ["d"], ["b"], ["e"]] },
            { "count":9,  "ballot":[["c"], ["b"], ["a"], ["e"], ["d"]] },
            { "count":51, "ballot":[["c"], ["d"], ["e"], ["a"], ["b"]] },
            { "count":33, "ballot":[["c"], ["e"], ["b"], ["d"], ["a"]] },
            { "count":42, "ballot":[["d"], ["a"], ["c"], ["e"], ["b"]] },
            { "count":18, "ballot":[["d"], ["b"], ["e"], ["c"], ["a"]] },
            { "count":6,  "ballot":[["d"], ["c"], ["b"], ["a"], ["e"]] },
            { "count":54, "ballot":[["d"], ["e"], ["a"], ["b"], ["c"]] },
            { "count":57, "ballot":[["e"], ["a"], ["b"], ["c"], ["d"]] },
            { "count":36, "ballot":[["e"], ["b"], ["d"], ["a"], ["c"]] },
            { "count":24, "ballot":[["e"], ["c"], ["a"], ["d"], ["b"]] },
            { "count":3,  "ballot":[["e"], ["d"], ["c"], ["b"], ["a"]] },
        ]
        output = SchulzeSTV(input, 3, "grouping").results()
        
        # Run tests
        self.assertEqual(output['winners'], set(['a', 'd', 'e']))
            
    # http://en.wikipedia.org/wiki/Schulze_STV#Count_under_Schulze_STV
    def test_wiki_example_1(self):

        # Generate data
        input = [
            { "count":12, "ballot":[["Andrea"], ["Brad"], ["Carter"]] },
            { "count":26, "ballot":[["Andrea"], ["Carter"], ["Brad"]] },
            { "count":12, "ballot":[["Andrea"], ["Carter"], ["Brad"]] },
            { "count":13, "ballot":[["Carter"], ["Andrea"], ["Brad"]] },
            { "count":27, "ballot":[["Brad"]] },
        ]
        output = SchulzeSTV(input, 2, "grouping").results()
        
        # Run tests
        self.assertEqual(output, {
            'candidates': set(['Carter', 'Brad', 'Andrea']),
            'actions': [
                {'edges': set([(('Brad', 'Carter'), ('Andrea', 'Carter')), (('Brad', 'Carter'), ('Andrea', 'Brad'))])},
                {'nodes': set([('Brad', 'Carter')])},
                {'edges': set([(('Andrea', 'Carter'), ('Andrea', 'Brad'))])},
                {'nodes': set([('Andrea', 'Carter')])}
            ],
            'winners': set(['Andrea', 'Brad'])
        })
        
    # http://en.wikipedia.org/wiki/Schulze_STV#Count_under_Schulze_STV_2
    def test_wiki_example_2(self):

        # Generate data
        input = [
            { "count":12, "ballot":[["Andrea"], ["Brad"], ["Carter"]] },
            { "count":26, "ballot":[["Andrea"], ["Carter"], ["Brad"]] },
            { "count":12, "ballot":[["Carter"], ["Andrea"], ["Brad"]] },
            { "count":13, "ballot":[["Carter"], ["Andrea"], ["Brad"]] },
            { "count":27, "ballot":[["Brad"]] },
        ]
        output = SchulzeSTV(input, 2, "grouping").results()
        
        # Run tests
        self.assertEqual(output, {
            'candidates': set(['Carter', 'Brad', 'Andrea']),
            'actions': [
                {'edges': set([(('Brad', 'Carter'), ('Andrea', 'Carter')), (('Brad', 'Carter'), ('Andrea', 'Brad'))])},
                {'nodes': set([('Brad', 'Carter')])},
                {'edges': set([(('Andrea', 'Carter'), ('Andrea', 'Brad'))])},
                {'nodes': set([('Andrea', 'Carter')])}
            ],
            'winners': set(['Andrea', 'Brad'])
        })

    #
    def test_one_ballot_one_winner(self):

        # Generate data
        input = [
            { "count":1, "ballot":{"a":1, "b":1, "c":3}}
        ]
        output = SchulzeSTV(input, 1, "rating").results()
        
        # Run tests
        self.assertEqual(output['winners'], set(["c"]))
    
    # This example ensures that vote management strength calculations are
    # calculated correctly.
    def test_one_ballot_two_winners(self):

        # Generate data
        input = [
            { "count":1, "ballot":{"Metal":1, "Paper":1, "Plastic":2, "Wood":2 }},
        ]
        output = SchulzeSTV(input, 2, "ranking").results()
        
        # Run tests
        self.assertEqual(output, {
            'candidates': set(['Paper', 'Wood', 'Metal', 'Plastic']),
            'actions': [{'nodes': set([
                ('Paper', 'Plastic'),
                ('Metal', 'Plastic'),
                ('Paper', 'Wood'),
                ('Metal', 'Wood'),
                ('Plastic', 'Wood')
            ])}],
            'winners': set(['Paper', 'Metal'])
        })
    
    # This example ensures that the proportional completion round correctly
    # accounts for sparse pattern weights.
    def test_two_ballots_two_winners(self):

        # Generate data
        input = [
            { "count":1, "ballot":{"Metal":2, "Paper":1, "Plastic":2, "Wood":2 }},
            { "count":1, "ballot":{"Metal":2, "Paper":2, "Plastic":2, "Wood":1 }}
        ]
        output = SchulzeSTV(input, 2, "ranking").results()
        
        # Run tests
        self.assertEqual(output, {
            "candidates": set(['Metal', 'Wood', 'Plastic', 'Paper']),
            "actions": [{'nodes': set([
                ('Paper', 'Plastic'),
                ('Metal', 'Plastic'),
                ('Metal', 'Paper'),
                ('Plastic', 'Wood'),
                ('Metal', 'Wood')
            ])}],
            "winners": set(['Paper', 'Wood']),
        })      

    # 
    def test_happenstance_example(self):

        # Generate data
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9 }}
        ]
        output = SchulzeSTV(input, 2, "ranking").results()
        
        # Run tests
        self.assertEqual(output["tied_winners"],
             set([('D', 'E'), ('B', 'E'), ('C', 'E'), ('B', 'D')])
        )

if __name__ == "__main__":
    unittest.main()
