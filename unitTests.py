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

from pluralityAtLarge import PluralityAtLarge
from plurality import Plurality
from instantRunoffVote import InstantRunoffVote
from singleTransferableVote import SingleTransferableVote 
from rankedPairs import RankedPairs
from schulzeMethod import SchulzeMethod
from schulzeSTV import SchulzeSTV
import unittest

class TestPlurality(unittest.TestCase):
    
    # Plurality, no ties
    def testNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":22, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = Plurality.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 23, 'c2': 22, 'c1': 26},
            'winners': set(['c1'])
        })
    
        
    # Plurality, alternate ballot format
    def testAlternateBallotFormat(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1"] },
            { "count":22, "ballot":["c2"] },
            { "count":23, "ballot":["c3"] }
        ]
        output = Plurality.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 23, 'c2': 22, 'c1': 26},
            'winners': set(['c1'])
        })
        

    # Plurality, irrelevant ties
    def testIrrelevantTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":23, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = Plurality.calculateWinner(input)

        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 23, 'c2': 23, 'c1': 26},
            'winners': set(['c1'])
        })


    # Plurality, relevant ties
    def testRelevantTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":26, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = Plurality.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output["tallies"], {'c1':26, 'c2':26, 'c3':23})
        self.assertEqual(output["tiedWinners"], set(['c1', 'c2']))
        self.assert_(list(output["winners"])[0] in output["tiedWinners"])
        self.assertEqual(len(output["tieBreaker"]), 3)


class TestInstantRunoff(unittest.TestCase):
    
    # IRV, no ties
    def testNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":23, "ballot":["c3", "c1", "c2"] }
        ]
        output = InstantRunoffVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 35,
            'rounds': [
                {'tallies': {'c3': 23, 'c2': 20, 'c1': 26}, 'loser': 'c2'}
            ],
            'winners': set(['c3'])
        })

    
    # IRV, ties
    def testTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":20, "ballot":["c3", "c1", "c2"] }
        ]
        output = InstantRunoffVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output["quota"], 34)
        self.assertEqual(len(output["rounds"]), 1)
        self.assertEqual(len(output["rounds"][0]), 3)
        self.assertEqual(output["rounds"][0]["tallies"], {'c1': 26, 'c2': 20, 'c3': 20})
        self.assertEqual(output["rounds"][0]["tiedLosers"], set(['c2','c3']))
        self.assert_(output["rounds"][0]["loser"] in output["rounds"][0]["tiedLosers"])
        self.assertEqual(len(output["tieBreaker"]), 3)


    # IRV, no rounds
    def testLandslide(self):
        
        # Generate data
        input = [
            { "count":56, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":20, "ballot":["c3", "c1", "c2"] }
        ]
        output = InstantRunoffVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 49,
            'rounds': [],
            'winners': set(['c1'])
        })


class TestRankedPairs(unittest.TestCase):
    
    # Ranked Pairs, cycle
    def testNoCycle(self):
        
        # Generate data
        input = [
            { "count":80, "ballot":[["c1", "c2"], ["c3"]] },
            { "count":50, "ballot":[["c2"], ["c3", "c1"]] },
            { "count":40, "ballot":[["c3"], ["c1"], ["c2"]] }
        ]
        output = RankedPairs.calculateWinner(input)
        
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
            'strongPairs': {
                ('c2', 'c3'): 130,
                ('c1', 'c3'): 80,
                ('c2', 'c1'): 50
            },
            'winners': set(['c2'])
        })
        

    # Ranked Pairs, cycle
    def testCycle(self):
        
        # Generate data
        input = [
            { "count":80, "ballot":[["c1"], ["c2"], ["c3"]] },
            { "count":50, "ballot":[["c2"], ["c3"], ["c1"]] },
            { "count":40, "ballot":[["c3"], ["c1"], ["c2"]] }
        ]
        output = RankedPairs.calculateWinner(input)
        
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
            'strongPairs': {
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


class TestSchulzeMethod(unittest.TestCase):
    
    # Schulze Method, example from Wikipedia
    # http://en.wikipedia.org/wiki/Schulze_method#The_Schwartz_set_heuristic
    def testWikiExample(self):
        
        # Generate data
        input = [
            { "count":3, "ballot":[["A"], ["C"], ["D"], ["B"]] },
            { "count":9, "ballot":[["B"], ["A"], ["C"], ["D"]] },
            { "count":8, "ballot":[["C"], ["D"], ["A"], ["B"]] },
            { "count":5, "ballot":[["D"], ["A"], ["B"], ["C"]] },
            { "count":5, "ballot":[["D"], ["B"], ["C"], ["A"]] }
        ]
        output = SchulzeMethod.calculateWinner(input)
        
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
            'strongPairs': {
                ('D', 'B'): 21,
                ('C', 'D'): 20,
                ('B', 'C'): 19,
                ('D', 'A'): 18,
                ('A', 'C'): 17,
                ('A', 'B'): 16,
            },
            'actions': [
                ['edges', set([('A', 'B')])],
                ['edges', set([('A', 'C')])],
                ['nodes', set(['A'])],
                ['edges', set([('B', 'C')])],
                ['nodes', set(['B', 'D'])]
            ],
            'winners': 'C'
        })
            

class TestPluralityAtLarge(unittest.TestCase):
    
    
    # Plurality, no ties
    def testPluralityNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":22, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = PluralityAtLarge.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 23, 'c2': 22, 'c1': 26},
            'winners': set(['c1'])
        })
    
        
    # Plurality, alternate ballot format
    def testPluralityAlternateBallotFormat(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1"] },
            { "count":22, "ballot":["c2"] },
            { "count":23, "ballot":["c3"] }
        ]
        output = PluralityAtLarge.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 23, 'c2': 22, 'c1': 26},
            'winners': set(['c1'])
        })
        

    # Plurality, irrelevant ties
    def PluralitytestIrrelevantTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":23, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = PluralityAtLarge.calculateWinner(input)

        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 23, 'c2': 23, 'c1': 26},
            'winners': set(['c1'])
        })


    # Plurality, relevant ties
    def testPluralityRelevantTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":26, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = PluralityAtLarge.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output["tallies"], {'c1':26, 'c2':26, 'c3':23})
        self.assertEqual(output["tiedWinners"], set(['c1', 'c2']))
        self.assert_(list(output["winners"])[0] in output["tiedWinners"])
        self.assertEqual(len(output["tieBreaker"]), 3)

    
    # Plurality at Large, no ties
    def testPluralityAtLargeNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2"] },
            { "count":22, "ballot":["c1", "c3"] },
            { "count":23, "ballot":["c2", "c3"] }
        ]
        output = PluralityAtLarge.calculateWinner(input, 2)
        
        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 45, 'c2': 49, 'c1': 48},
            'winners': set(['c2', 'c1'])
        })
      
            
    # Plurality at Large, irrelevant ties
    def testPluralityAtLargeIrrelevantTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2"] },
            { "count":22, "ballot":["c1", "c3"] },
            { "count":22, "ballot":["c2", "c3"] },
            { "count":11, "ballot":["c4", "c5"] }
        ]
        output = PluralityAtLarge.calculateWinner(input, 2)
        
        # Run tests
        self.assertEqual(output, {
            'tallies': {'c3': 44, 'c2': 48, 'c1': 48, 'c5': 11, 'c4': 11},
            'winners': set(['c2', 'c1'])
        })
        
            
    # Plurality at Large, irrelevant ties
    def testPluralityAtLargeRelevantTies(self):
        
        # Generate data
        input = [
            { "count":30, "ballot":["c1", "c2"] },
            { "count":22, "ballot":["c3", "c1"] },
            { "count":22, "ballot":["c2", "c3"] },
            { "count":4, "ballot":["c4", "c1"] },
            { "count":8, "ballot":["c3", "c4"] },
        ]
        output = PluralityAtLarge.calculateWinner(input, 2)

        # Run tests
        self.assertEqual(output["tallies"], {'c3': 52, 'c2': 52, 'c1': 56, 'c4': 12})
        self.assertEqual(len(output["tieBreaker"]), 4)
        self.assertEqual(output["tiedWinners"], set(['c2','c3']))
        self.assert_("c1" in output["winners"] and ("c2" in output["winners"] or "c3" in output["winners"]))
        self.assertEqual(len(output), 4)
        

class TestSingleTransferableVote(unittest.TestCase):
    
    # IRV, no ties
    def testIRVNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":23, "ballot":["c3", "c1", "c2"] }
        ]
        output = SingleTransferableVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'winners': set(['c3']),
            'rounds': [
                {'tallies': {'c3': 23.0, 'c2': 20.0, 'c1': 26.0}, 'quota': 35, 'loser': 'c2'},
                {'tallies': {'c3': 43.0, 'c1': 26.0}, 'winners': set(['c3']), 'quota': 35}
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
        output = SingleTransferableVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(len(output["rounds"]), 2)
        self.assertEqual(len(output["rounds"][0]), 4)
        self.assertEqual(output["rounds"][0]["quota"], 34)
        self.assertEqual(output["rounds"][0]["tallies"], {'c1': 26, 'c2': 20, 'c3': 20})
        self.assertEqual(output["rounds"][0]["tiedLosers"], set(['c2','c3']))
        self.assert_(output["rounds"][0]["loser"] in output["rounds"][0]["tiedLosers"])
        self.assertEqual(output["rounds"][1]["quota"], 34)
        self.assertEqual(len(output["rounds"][1]["tallies"]), 2)
        self.assertEqual(len(output["rounds"][1]["winners"]), 1)
        self.assertEqual(len(output["tieBreaker"]), 3)


    # IRV, no rounds
    def testIRVLandslide(self):
        
        # Generate data
        input = [
            { "count":56, "ballot":["c1", "c2", "c3"] },
            { "count":20, "ballot":["c2", "c3", "c1"] },
            { "count":20, "ballot":["c3", "c1", "c2"] }
        ]
        output = SingleTransferableVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output, {
            'winners': set(['c1']),
            'rounds': [{
                'quota': 49,
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
        output = SingleTransferableVote.calculateWinner(input, 2)
        
        # Run tests
        self.assertEqual(output, {
            'rounds': [{
                'quota': 39,
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
        output = SingleTransferableVote.calculateWinner(input, 3)
        
        # Run tests
        self.assertEqual(output, {
            'rounds': [
                {
                    'quota': 6,
                    'tallies': {'orange': 4.0, 'strawberry': 1.0, 'pear': 2.0, 'sweets': 1.0, 'chocolate': 12.0},
                    'winners': set(['chocolate'])
                },
                {
                    'quota': 5,
                    'tallies': {'orange': 4.0, 'strawberry': 5.0, 'pear': 2.0, 'sweets': 3.0},
                    'winners': set(['strawberry'])
                },
                {
                    'quota': 5,
                    'tallies': {'orange': 4.0, 'pear': 2.0, 'sweets': 3.0},
                    'loser': 'pear'
                },
                {
                    'quota': 5,
                    'tallies': {'orange': 6.0, 'sweets': 3.0},
                    'winners': set(['orange'])
                }
            ],
            'winners': set(['orange', 'strawberry', 'chocolate'])
        })
        

class TestSchulzeSTV(unittest.TestCase):
    
    # Schulze STV, example from Markus' part 2 of 5: Free Riding and Vote Management 
    def testWikiExample(self):
        
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
        
        # Generate data
        #input = [
        #    { "count":60, "ballot":[["a"], ["b"], ["c"], ["d"], ["e"]] },
        #    { "count":45, "ballot":[["a"], ["c"], ["e"], ["b"], ["d"]] },
        #    { "count":30, "ballot":[["a"], ["d"], ["b"], ["e"], ["c"]] },
        #    { "count":15, "ballot":[["a"], ["e"], ["d"], ["c"], ["b"]] },
        #    { "count":12, "ballot":[["b"], ["a"], ["e"], ["d"], ["c"]] },
        #    { "count":48, "ballot":[["b"], ["c"], ["d"], ["e"], ["a"]] },
        #    { "count":39, "ballot":[["b"], ["d"], ["a"], ["c"], ["e"]] },
        #    { "count":21, "ballot":[["b"], ["e"], ["c"], ["a"], ["d"]] },
        #    { "count":27, "ballot":[["c"], ["a"], ["d"], ["b"], ["e"]] },
        #    { "count":9,  "ballot":[["c"], ["b"], ["a"], ["e"], ["d"]] },
        #    { "count":51, "ballot":[["c"], ["d"], ["e"], ["a"], ["b"]] },
        #    { "count":33, "ballot":[["c"], ["e"], ["b"], ["d"], ["a"]] },
        #    { "count":42, "ballot":[["d"], ["a"], ["c"], ["e"], ["b"]] },
        #    { "count":18, "ballot":[["d"], ["b"], ["e"], ["c"], ["a"]] },
        #    { "count":6,  "ballot":[["d"], ["c"], ["b"], ["a"], ["e"]] },
        #    { "count":54, "ballot":[["d"], ["e"], ["a"], ["b"], ["c"]] },
        #    { "count":57, "ballot":[["e"], ["a"], ["b"], ["c"], ["d"]] },
        #    { "count":36, "ballot":[["e"], ["b"], ["d"], ["a"], ["c"]] },
        #    { "count":24, "ballot":[["e"], ["c"], ["a"], ["d"], ["b"]] },
        #    { "count":3,  "ballot":[["e"], ["d"], ["c"], ["b"], ["a"]] },
        #]
        
        # First
        # r(V(d,{a,b,c})) = 169
        
        # Second
        # r(V(abc -> abd)) = 169
        # r(V(abc -> acd)) = 169
        # r(V(abc -> bcd)) = 169

        output = SchulzeSTV.calculateWinner(input)
        
        # Run tests
        

if __name__ == "__main__":
    unittest.main()