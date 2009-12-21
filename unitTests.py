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
    
     
    # http://en.wikipedia.org/wiki/Schulze_method#Example
    def testWikiExample2(self):

        # Generate data
        input = [
            { "count":5, "ballot":[["A"], ["C"], ["B"], ["E"], ["D"]] },
            { "count":5, "ballot":[["A"], ["D"], ["E"], ["C"], ["B"]] },
            { "count":8, "ballot":[["B"], ["E"], ["D"], ["A"], ["C"]] },
            { "count":3, "ballot":[["C"], ["A"], ["B"], ["E"], ["D"]] },
            { "count":7, "ballot":[["C"], ["A"], ["E"], ["B"], ["D"]] },
            { "count":2, "ballot":[["C"], ["B"], ["A"], ["D"], ["E"]] },
            { "count":7, "ballot":[["D"], ["C"], ["E"], ["B"], ["A"]] },
            { "count":8, "ballot":[["E"], ["B"], ["A"], ["D"], ["C"]] }
        ]
        output = SchulzeMethod.calculateWinner(input)
        
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
            'strongPairs': {
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
                ['edges', set([('E', 'A')])],
                ['edges', set([('C', 'E')])],
                ['nodes', set(['A', 'C', 'B', 'D'])]
            ],
            'winners': 'E'
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
        output = SingleTransferableVote.calculateWinner(input)
        
        # Run tests
        self.assertEqual(output["quota"], 34)
        self.assertEqual(len(output["rounds"]), 2)
        self.assertEqual(len(output["rounds"][0]), 3)
        self.assertEqual(output["rounds"][0]["tallies"], {'c1': 26, 'c2': 20, 'c3': 20})
        self.assertEqual(output["rounds"][0]["tiedLosers"], set(['c2','c3']))
        self.assert_(output["rounds"][0]["loser"] in output["rounds"][0]["tiedLosers"])
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
        output = SingleTransferableVote.calculateWinner(input, 2)
        
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
        output = SingleTransferableVote.calculateWinner(input, 3)
        
        # Run tests
        self.assertEqual(output, {
            'quota': 6,
            'rounds': [
                {'tallies': {'orange': 4.0, 'strawberry': 1.0, 'pear': 2.0, 'sweets': 1.0, 'chocolate': 12.0},'winners': set(['chocolate'])},
                {'tallies': {'orange': 4.0, 'strawberry': 5.0, 'pear': 2.0, 'sweets': 3.0}, 'loser': 'pear'},
                {'tallies': {'orange': 6.0, 'strawberry': 5.0, 'sweets': 3.0}, 'winners': set(['orange'])},
                {'tallies': {'strawberry': 5.0, 'sweets': 3.0}, 'loser': 'sweets'}
            ],
            'remainingCandidates': set(['strawberry']),
            'winners': set(['orange', 'strawberry', 'chocolate'])
        })


class TestSchulzeSTV(unittest.TestCase):
    
    # Schulze STV, example from Markus' part 2 of 5: Free Riding and Vote Management 
    def testSchulze2Example(self):
        return
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
        output = SchulzeSTV.calculateWinner(input, 3, "preferenceSets")
        
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
        #   r(V(d,{a,b,c})) = 169
        # Second
        #   r(V(abc -> abd)) = 169
        #   r(V(abc -> acd)) = 169
        #   r(V(abc -> bcd)) = 169
        
        # Run tests
        
    
    # Schulze STV, example from Markus' part 3 of 5: Implementing the Schulze
    # STV Method. See calcul01.pdf (Abstract: In this paper, we illustrate the
    # concept of “proportional completion”.) 
    def testSchulzeSTVProportionalCompletion(self):
        input = [
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  4, "G":  3, "H":  2, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  4, "D":  5, "E":  3, "F":  9, "G":  6, "H": 10, "I":  8, "J":  7}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C": 10, "D":  7, "E":  3, "F":  8, "G":  5, "H":  9, "I":  1, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E":  5, "F":  4, "G":  6, "H":  7, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C":  3, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C":  1, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I":  4, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  1, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  5, "C": 99, "D": 99, "E":  1, "F":  4, "G":  2, "H": 99, "I":  3, "J":  6}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C":  5, "D": 99, "E":  1, "F": 99, "G":  2, "H":  3, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  7, "B":  9, "C":  6, "D": 10, "E":  1, "F":  5, "G":  3, "H":  4, "I":  8, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B":  5, "C":  3, "D":  9, "E":  1, "F": 10, "G":  2, "H":  6, "I":  8, "J":  7}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  2, "F": 99, "G":  3, "H": 99, "I":  1, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  4, "D": 99, "E":  2, "F": 99, "G":  3, "H": 99, "I":  1, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  5, "D": 99, "E":  1, "F": 99, "G":  4, "H": 99, "I":  6, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  1, "F":  4, "G":  2, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  6, "E": 99, "F":  4, "G":  5, "H":  1, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  5, "E": 99, "F":  2, "G":  3, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  9, "C":  7, "D":  5, "E":  8, "F":  2, "G": 10, "H":  6, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  7, "C":  3, "D":  6, "E":  8, "F":  2, "G": 10, "H":  5, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  6, "E":  3, "F":  2, "G": 99, "H":  5, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  5, "C": 99, "D":  4, "E": 99, "F":  3, "G": 99, "H": 99, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  4, "E": 99, "F":  3, "G": 99, "H": 99, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 10, "C":  9, "D":  8, "E":  7, "F":  3, "G":  5, "H":  6, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  6, "E": 99, "F":  3, "G": 99, "H":  5, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C": 99, "D":  2, "E": 99, "F": 99, "G": 99, "H":  5, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  8, "B":  9, "C":  7, "D":  2, "E":  3, "F":  4, "G":  5, "H":  6, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  7, "C":  6, "D":  2, "E":  3, "F":  4, "G": 10, "H":  9, "I":  8, "J":  1}},
            { "count":1, "ballot":{"A": 10, "B":  8, "C":  4, "D":  2, "E":  3, "F":  9, "G":  7, "H":  5, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  6, "C": 99, "D":  2, "E":  5, "F":  3, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G":  3, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  9, "C":  7, "D":  2, "E":  4, "F":  8, "G":  6, "H": 10, "I":  5, "J":  1}},
            { "count":1, "ballot":{"A":  1, "B":  5, "C":  2, "D": 99, "E": 99, "F": 99, "G":  3, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  7, "C":  5, "D":  3, "E":  9, "F":  6, "G":  8, "H":  4, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  7, "C":  5, "D":  6, "E":  3, "F":  2, "G":  8, "H":  9, "I": 10, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  4, "D":  3, "E": 10, "F":  9, "G":  5, "H":  8, "I":  7, "J":  6}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  3, "E":  6, "F":  2, "G": 99, "H":  4, "I": 99, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  8, "C":  5, "D":  2, "E":  4, "F":  3, "G": 10, "H":  9, "I":  7, "J":  6}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  2, "E":  3, "F":  5, "G": 99, "H": 99, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  3, "D":  5, "E":  7, "F":  4, "G":  8, "H":  9, "I": 10, "J":  6}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  7, "D":  4, "E":  6, "F":  5, "G":  9, "H": 10, "I":  8, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  3, "D":  5, "E":  4, "F":  6, "G": 10, "H": 11, "I": 12, "J":  7}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C":  8, "D":  7, "E":  6, "F":  5, "G":  4, "H":  2, "I":  9, "J": 10}},
            { "count":1, "ballot":{"A":  1, "B":  7, "C":  6, "D":  4, "E":  5, "F":  2, "G":  8, "H": 10, "I":  9, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C":  7, "D":  6, "E": 10, "F":  4, "G":  9, "H":  5, "I":  8, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  8, "C": 10, "D":  4, "E":  7, "F":  2, "G":  3, "H":  9, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  6, "D": 99, "E":  2, "F":  3, "G": 99, "H":  7, "I":  5, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C":  6, "D": 10, "E":  7, "F":  9, "G":  5, "H":  2, "I":  8, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B": 10, "C":  4, "D":  9, "E":  7, "F":  2, "G":  5, "H":  8, "I":  3, "J":  6}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H":  3, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C": 99, "D": 99, "E": 99, "F": 99, "G":  3, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  4, "B":  5, "C": 99, "D": 99, "E":  6, "F": 99, "G": 99, "H":  3, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  5, "C":  6, "D": 10, "E":  8, "F":  9, "G":  7, "H":  3, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  5, "C":  9, "D":  6, "E":  7, "F":  8, "G": 10, "H":  2, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A":  6, "B":  3, "C":  5, "D":  7, "E": 10, "F":  4, "G":  8, "H":  2, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A": 10, "B":  3, "C":  4, "D":  9, "E":  5, "F":  6, "G":  8, "H":  2, "I":  7, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C":  2, "D":  7, "E":  8, "F":  9, "G": 10, "H":  5, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A":  7, "B":  3, "C":  6, "D":  9, "E":  2, "F":  8, "G":  5, "H": 10, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  3, "C":  7, "D":  9, "E":  2, "F":  6, "G": 10, "H":  5, "I":  8, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  3, "C": 10, "D":  7, "E":  2, "F":  9, "G":  8, "H":  6, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C":  2, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  1, "D":  6, "E":  2, "F": 99, "G":  3, "H": 99, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  4, "D":  3, "E":  1, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  9, "C":  8, "D":  5, "E":  1, "F":  6, "G":  3, "H":  7, "I": 10, "J":  4}},
            { "count":1, "ballot":{"A":  6, "B":  3, "C":  7, "D":  9, "E":  2, "F":  8, "G":  1, "H": 10, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  4, "B":  9, "C":  6, "D": 10, "E":  3, "F":  7, "G":  1, "H":  8, "I":  5, "J":  2}},
            { "count":1, "ballot":{"A":  3, "B":  9, "C":  5, "D":  6, "E":  4, "F":  8, "G":  1, "H":  7, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H":  4, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  7, "B":  4, "C":  8, "D":  5, "E":  9, "F":  6, "G":  1, "H":  2, "I": 10, "J":  3}},
            { "count":1, "ballot":{"A":  9, "B": 10, "C":  8, "D":  5, "E":  7, "F":  6, "G":  1, "H":  2, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  2, "E":  3, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  7, "B":  8, "C": 10, "D":  3, "E":  2, "F":  6, "G":  1, "H":  9, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  4, "B":  3, "C":  2, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  7, "C":  4, "D":  5, "E":  6, "F":  8, "G":  1, "H":  9, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B": 10, "C":  6, "D":  7, "E":  2, "F":  8, "G":  1, "H":  9, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C":  4, "D":  6, "E":  7, "F": 10, "G":  1, "H":  8, "I":  9, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  3, "E": 99, "F": 99, "G":  1, "H":  2, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  4, "C":  3, "D":  9, "E": 10, "F":  8, "G":  1, "H":  5, "I":  7, "J":  6}},
            { "count":1, "ballot":{"A":  4, "B":  7, "C":  2, "D":  6, "E":  5, "F":  8, "G":  1, "H":  9, "I": 10, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C": 99, "D": 99, "E":  3, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C": 99, "D": 99, "E":  4, "F": 99, "G":  1, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C": 99, "D":  2, "E":  4, "F": 99, "G":  1, "H":  3, "I": 99, "J":  6}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I":  2, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  4, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  7, "B":  3, "C":  4, "D":  2, "E":  9, "F":  6, "G":  1, "H":  8, "I": 10, "J":  5}},
            { "count":1, "ballot":{"A":  2, "B":  8, "C":  5, "D":  7, "E":  6, "F":  3, "G":  1, "H": 10, "I":  9, "J":  4}},
            { "count":1, "ballot":{"A":  7, "B": 10, "C":  6, "D":  9, "E":  5, "F":  4, "G":  1, "H":  8, "I":  3, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H":  3, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F":  3, "G":  1, "H": 99, "I":  2, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  2, "E": 99, "F":  3, "G":  1, "H":  4, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  1, "H": 99, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  6, "B": 10, "C":  8, "D":  9, "E":  7, "F":  5, "G":  1, "H":  4, "I":  2, "J":  3}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C": 99, "D":  4, "E": 99, "F": 99, "G":  1, "H":  3, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  3, "E":  5, "F": 99, "G":  1, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  1, "H": 99, "I":  5, "J":  4}},
            { "count":1, "ballot":{"A":  4, "B":  3, "C": 99, "D":  2, "E": 99, "F": 99, "G":  1, "H": 99, "I":  5, "J":  6}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  4, "E": 99, "F":  2, "G":  1, "H": 99, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D":  2, "E": 99, "F":  3, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C":  4, "D": 99, "E":  5, "F": 99, "G":  1, "H":  6, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 10, "B":  5, "C":  3, "D":  2, "E":  4, "F":  9, "G":  1, "H":  7, "I":  8, "J":  6}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C":  2, "D":  1, "E": 99, "F":  4, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I":  4, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H":  3, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  6, "B":  5, "C": 10, "D":  1, "E":  3, "F":  7, "G":  2, "H":  8, "I":  9, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E":  4, "F": 99, "G": 99, "H": 99, "I":  3, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D":  1, "E": 99, "F":  3, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B":  3, "C": 99, "D":  1, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C":  6, "D":  1, "E":  3, "F":  4, "G":  7, "H": 10, "I":  9, "J":  8}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  1, "E": 99, "F":  3, "G": 99, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C": 99, "D":  1, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F":  2, "G":  4, "H": 99, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  4, "B":  5, "C":  7, "D":  1, "E":  2, "F":  9, "G":  6, "H":  8, "I":  3, "J": 10}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H":  2, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 99, "D":  1, "E": 99, "F": 99, "G":  5, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  3, "B": 10, "C":  6, "D":  1, "E":  4, "F":  8, "G":  7, "H":  9, "I":  5, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  4, "D":  1, "E": 99, "F":  5, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H":  3, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E":  2, "F":  3, "G": 99, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  3, "B":  2, "C":  7, "D":  1, "E":  6, "F":  9, "G": 10, "H":  5, "I":  8, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C":  6, "D":  1, "E": 99, "F":  3, "G":  4, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C":  8, "D":  1, "E":  6, "F":  9, "G":  7, "H":  3, "I":  2, "J": 10}},
            { "count":1, "ballot":{"A":  2, "B":  9, "C":  5, "D":  1, "E":  3, "F": 10, "G":  8, "H":  6, "I":  4, "J":  7}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F":  2, "G": 99, "H":  3, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E":  2, "F":  3, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  9, "B":  7, "C":  8, "D":  1, "E":  2, "F":  6, "G":  3, "H": 10, "I":  5, "J":  4}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C":  6, "D":  1, "E":  7, "F":  9, "G":  2, "H": 10, "I":  8, "J":  5}},
            { "count":1, "ballot":{"A":  5, "B":  6, "C":  7, "D":  1, "E":  2, "F":  9, "G":  3, "H": 10, "I":  4, "J":  8}},
            { "count":1, "ballot":{"A":  3, "B":  9, "C":  6, "D":  1, "E": 10, "F":  4, "G":  2, "H":  7, "I":  8, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D":  1, "E":  5, "F":  3, "G": 99, "H": 99, "I":  2, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C":  9, "D":  1, "E":  8, "F":  5, "G": 10, "H":  3, "I":  7, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  3, "D":  1, "E": 99, "F": 99, "G": 99, "H": 99, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  1, "E": 99, "F":  2, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  1, "E":  4, "F": 99, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  3, "B":  6, "C":  5, "D":  2, "E":  7, "F": 10, "G":  8, "H":  9, "I":  1, "J":  4}},
            { "count":1, "ballot":{"A":  8, "B":  6, "C":  7, "D":  4, "E":  5, "F": 10, "G":  9, "H":  3, "I":  1, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  3, "E": 99, "F": 99, "G":  4, "H":  1, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  7, "B": 99, "C":  1, "D":  3, "E":  6, "F":  5, "G":  4, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  1, "D":  2, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  5, "C":  2, "D":  3, "E": 99, "F":  4, "G": 99, "H": 99, "I":  1, "J":  6}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  2, "D":  3, "E":  5, "F": 99, "G":  4, "H": 99, "I":  1, "J":  6}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C":  9, "D":  2, "E":  1, "F":  6, "G":  7, "H":  8, "I": 10, "J":  3}},
            { "count":1, "ballot":{"A":  4, "B": 10, "C":  5, "D":  2, "E":  1, "F":  6, "G":  3, "H":  9, "I":  8, "J":  7}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  2, "E":  1, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  3, "E":  1, "F": 99, "G":  5, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B":  9, "C":  7, "D":  5, "E":  1, "F":  8, "G":  6, "H":  4, "I": 10, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  1, "D":  3, "E":  2, "F":  4, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  8, "C":  9, "D":  4, "E": 10, "F":  1, "G":  5, "H":  2, "I":  6, "J":  7}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  6, "D":  4, "E":  3, "F":  1, "G": 99, "H":  5, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B":  8, "C":  7, "D":  3, "E":  4, "F":  1, "G":  5, "H":  9, "I": 10, "J":  6}},
            { "count":1, "ballot":{"A":  8, "B":  6, "C":  5, "D":  3, "E": 10, "F":  1, "G":  4, "H":  7, "I":  9, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C":  6, "D":  3, "E": 99, "F":  1, "G": 99, "H":  4, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  6, "B":  8, "C":  5, "D":  7, "E":  4, "F":  1, "G":  9, "H":  3, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  3, "E": 99, "F":  1, "G": 99, "H": 99, "I":  5, "J":  2}},
            { "count":1, "ballot":{"A":  6, "B":  8, "C":  7, "D":  2, "E":  9, "F":  1, "G": 10, "H":  5, "I":  4, "J":  3}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  3, "E": 99, "F":  1, "G": 99, "H": 99, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A":  8, "B":  9, "C":  6, "D":  2, "E":  4, "F":  1, "G":  3, "H": 10, "I":  5, "J":  7}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  5, "E":  3, "F":  1, "G":  4, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  5, "C": 99, "D":  3, "E":  4, "F":  1, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C":  7, "D":  3, "E":  5, "F":  1, "G":  8, "H": 10, "I":  9, "J":  4}},
            { "count":1, "ballot":{"A":  9, "B": 10, "C":  3, "D":  8, "E":  2, "F":  1, "G":  4, "H":  7, "I":  5, "J":  6}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  2, "E": 99, "F":  1, "G":  3, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  9, "B":  6, "C":  4, "D":  5, "E":  2, "F":  3, "G": 10, "H":  8, "I":  1, "J":  7}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C":  4, "D": 99, "E": 99, "F":  3, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  4, "D": 99, "E":  6, "F":  3, "G":  5, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F":  5, "G":  6, "H":  2, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F":  4, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H":  3, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  3, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  3, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  4, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C":  5, "D":  8, "E":  7, "F":  2, "G":  6, "H":  9, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  7, "B":  8, "C":  9, "D": 10, "E":  3, "F":  6, "G":  4, "H":  2, "I":  5, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D": 99, "E":  2, "F":  3, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  9, "C":  7, "D": 10, "E":  2, "F":  5, "G":  8, "H":  3, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  5, "C":  8, "D":  6, "E": 10, "F":  2, "G":  7, "H":  9, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A": 10, "B":  5, "C":  6, "D":  9, "E":  4, "F":  3, "G":  7, "H":  8, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  6, "B":  4, "C": 99, "D":  5, "E": 99, "F":  3, "G": 99, "H":  7, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  8, "C":  6, "D": 10, "E":  4, "F":  3, "G":  9, "H":  7, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  7, "C": 99, "D": 99, "E":  5, "F":  3, "G":  4, "H":  6, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B": 10, "C":  9, "D":  4, "E":  6, "F":  7, "G":  3, "H":  8, "I":  1, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  3, "F": 99, "G":  2, "H": 99, "I":  1, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F":  3, "G":  2, "H": 99, "I":  1, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H":  1, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  9, "C":  1, "D":  5, "E": 10, "F":  6, "G":  2, "H":  4, "I":  8, "J":  7}},
            { "count":1, "ballot":{"A":  2, "B":  7, "C":  1, "D":  5, "E":  6, "F":  4, "G":  3, "H":  8, "I":  9, "J": 10}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C":  1, "D":  7, "E":  9, "F": 10, "G":  3, "H":  8, "I":  5, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B":  5, "C":  1, "D": 99, "E": 99, "F": 99, "G":  2, "H":  3, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  1, "D": 99, "E":  4, "F": 99, "G":  3, "H": 99, "I":  5, "J":  2}},
            { "count":1, "ballot":{"A":  9, "B": 10, "C":  1, "D":  8, "E":  7, "F":  3, "G":  2, "H":  5, "I":  4, "J":  6}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  3, "D":  5, "E": 99, "F": 99, "G":  4, "H":  1, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D": 99, "E":  3, "F": 99, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D": 99, "E":  3, "F": 99, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  2, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  2, "F": 99, "G": 99, "H":  3, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C":  5, "D":  8, "E":  3, "F":  9, "G":  7, "H":  1, "I": 10, "J":  4}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C":  4, "D": 99, "E": 99, "F":  2, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H":  2, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D": 99, "E": 99, "F":  2, "G":  1, "H":  3, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  5, "D": 99, "E":  6, "F":  4, "G":  1, "H": 99, "I":  3, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C":  6, "D": 99, "E":  8, "F":  2, "G":  1, "H":  7, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  8, "B": 10, "C":  3, "D":  6, "E":  7, "F":  2, "G":  1, "H":  4, "I":  9, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  3, "E": 99, "F":  2, "G":  1, "H": 99, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C":  5, "D": 10, "E":  6, "F":  9, "G":  1, "H":  8, "I":  7, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C": 10, "D":  8, "E":  7, "F":  4, "G":  1, "H":  5, "I":  9, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C": 99, "D":  2, "E": 99, "F":  4, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  3, "E":  4, "F": 99, "G": 99, "H": 99, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C":  5, "D":  4, "E": 99, "F": 99, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D":  3, "E": 99, "F": 99, "G": 99, "H":  2, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C":  2, "D":  4, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  9, "C":  2, "D":  6, "E":  5, "F":  7, "G":  8, "H":  3, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  7, "C":  4, "D":  6, "E":  5, "F":  9, "G":  8, "H":  2, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C": 99, "D":  3, "E":  2, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  1, "C": 99, "D": 99, "E": 99, "F":  5, "G":  4, "H": 99, "I":  6, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C": 99, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C": 99, "D": 99, "E": 99, "F":  3, "G": 99, "H": 99, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E": 99, "F": 99, "G":  3, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B":  1, "C":  2, "D":  3, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  5}},
            { "count":1, "ballot":{"A":  6, "B":  1, "C":  5, "D":  7, "E":  4, "F":  8, "G":  2, "H":  9, "I": 10, "J":  3}},
            { "count":1, "ballot":{"A":  9, "B":  1, "C":  5, "D": 10, "E":  4, "F":  2, "G":  6, "H":  8, "I":  7, "J":  3}},
            { "count":1, "ballot":{"A":  4, "B":  1, "C":  5, "D":  9, "E":  3, "F":  6, "G":  8, "H":  7, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E":  3, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C":  3, "D": 99, "E": 99, "F":  4, "G":  5, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E":  2, "F": 99, "G": 99, "H":  3, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  1, "C":  7, "D":  2, "E":  8, "F":  9, "G":  4, "H": 10, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E":  2, "F": 99, "G":  3, "H":  4, "I":  5, "J":  6}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C":  9, "D":  6, "E":  5, "F":  7, "G": 10, "H":  3, "I":  8, "J":  4}},
            { "count":1, "ballot":{"A":  7, "B":  1, "C":  8, "D":  3, "E":  6, "F":  4, "G":  5, "H":  9, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B":  1, "C":  6, "D":  7, "E":  2, "F": 10, "G":  3, "H":  9, "I":  8, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C":  8, "D":  5, "E":  9, "F":  6, "G": 10, "H":  7, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C":  3, "D": 10, "E":  4, "F":  5, "G":  7, "H":  6, "I":  8, "J":  9}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E":  2, "F":  4, "G": 99, "H":  3, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  6, "B":  1, "C":  4, "D":  8, "E":  7, "F":  2, "G":  5, "H": 10, "I":  9, "J":  3}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C":  9, "D": 10, "E":  7, "F":  6, "G":  4, "H":  5, "I":  8, "J":  3}},
            { "count":1, "ballot":{"A":  4, "B":  1, "C":  5, "D":  6, "E": 99, "F": 99, "G":  2, "H":  7, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C":  5, "D": 99, "E":  2, "F": 99, "G":  3, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  3, "B":  1, "C":  5, "D":  2, "E":  8, "F":  4, "G": 10, "H":  7, "I":  9, "J":  6}},
            { "count":1, "ballot":{"A":  6, "B":  1, "C":  5, "D":  7, "E":  4, "F":  8, "G":  3, "H":  9, "I":  2, "J": 10}},
            { "count":1, "ballot":{"A":  5, "B":  1, "C":  6, "D":  3, "E":  2, "F":  9, "G":  4, "H":  7, "I":  8, "J": 10}},
            { "count":1, "ballot":{"A":  9, "B":  1, "C":  6, "D":  5, "E":  3, "F": 10, "G":  2, "H":  4, "I":  7, "J":  8}},
            { "count":1, "ballot":{"A":  6, "B":  1, "C":  3, "D":  5, "E":  4, "F": 10, "G":  2, "H":  8, "I":  9, "J":  7}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E":  4, "F":  3, "G":  5, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C":  4, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E":  2, "F": 99, "G": 99, "H":  3, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E": 99, "F":  4, "G":  2, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  5, "B":  1, "C":  9, "D":  4, "E":  2, "F":  6, "G": 10, "H":  7, "I":  8, "J":  3}},
            { "count":1, "ballot":{"A":  2, "B":  1, "C":  8, "D":  7, "E":  6, "F":  5, "G":  9, "H": 10, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  3, "B":  1, "C":  7, "D":  6, "E":  9, "F":  5, "G":  4, "H":  8, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  9, "B":  2, "C":  8, "D":  3, "E":  7, "F": 10, "G":  4, "H":  6, "I":  1, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C": 99, "D":  4, "E": 99, "F":  5, "G": 99, "H":  1, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C":  2, "D": 99, "E":  6, "F": 99, "G":  5, "H":  1, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  7, "B":  4, "C":  2, "D": 10, "E":  5, "F":  9, "G":  6, "H":  1, "I":  3, "J":  8}},
            { "count":1, "ballot":{"A":  6, "B":  4, "C":  3, "D": 10, "E":  5, "F":  7, "G":  9, "H":  1, "I":  8, "J":  2}},
            { "count":1, "ballot":{"A":  3, "B":  2, "C":  1, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C":  1, "D": 99, "E": 99, "F":  3, "G": 99, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  9, "B":  5, "C":  8, "D":  7, "E":  2, "F":  6, "G": 10, "H":  1, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  4, "B":  2, "C":  8, "D":  7, "E":  1, "F": 10, "G":  9, "H":  5, "I":  3, "J":  6}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C": 99, "D": 99, "E":  1, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  4, "B":  5, "C":  6, "D":  8, "E":  3, "F":  9, "G": 10, "H":  1, "I":  7, "J":  2}},
            { "count":1, "ballot":{"A":  6, "B":  3, "C":  5, "D": 10, "E":  1, "F":  4, "G":  9, "H":  7, "I":  8, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B":  6, "C":  9, "D": 10, "E":  1, "F":  7, "G":  8, "H":  3, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  6, "B":  4, "C": 99, "D": 99, "E":  3, "F":  5, "G": 99, "H":  1, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  7, "B":  2, "C":  8, "D":  6, "E":  4, "F":  9, "G":  3, "H": 10, "I":  5, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  2, "C": 99, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  2, "C":  8, "D":  4, "E":  3, "F":  6, "G": 10, "H":  7, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A":  7, "B":  2, "C":  9, "D":  8, "E":  3, "F": 10, "G":  4, "H":  5, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C": 99, "D":  3, "E": 99, "F": 99, "G": 99, "H":  4, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  2, "C": 10, "D":  7, "E":  4, "F":  3, "G":  8, "H":  6, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  2, "C":  6, "D":  5, "E":  3, "F":  8, "G":  7, "H": 10, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  9, "D":  5, "E": 10, "F":  6, "G":  7, "H":  4, "I":  8, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  4, "C": 99, "D":  6, "E":  3, "F": 99, "G": 99, "H":  5, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  4, "C": 99, "D": 99, "E":  5, "F":  6, "G":  3, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 99, "D": 99, "E": 99, "F": 99, "G":  5, "H":  4, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 10, "D":  4, "E":  9, "F":  5, "G":  6, "H":  7, "I":  8, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E":  3, "F": 99, "G":  4, "H":  5, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F":  4, "G": 99, "H":  3, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  4, "D":  8, "E":  7, "F": 10, "G":  5, "H":  6, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F":  3, "G": 99, "H":  4, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F":  3, "G":  4, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  3, "D":  4, "E": 99, "F":  5, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E":  3, "F": 99, "G": 99, "H": 99, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C":  4, "D":  3, "E":  6, "F": 99, "G": 99, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 10, "C":  3, "D":  4, "E":  6, "F":  9, "G":  5, "H":  7, "I":  8, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  5, "D": 99, "E": 99, "F":  3, "G": 99, "H": 99, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  6, "D":  7, "E":  8, "F":  4, "G":  9, "H":  5, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H":  4, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H":  4, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 10, "D":  8, "E":  7, "F":  4, "G":  9, "H":  5, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F":  3, "G": 99, "H":  2, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 99, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  9, "C":  4, "D":  5, "E":  6, "F":  7, "G":  3, "H": 10, "I":  8, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  6, "D":  4, "E": 99, "F": 99, "G": 99, "H": 99, "I":  5, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  4, "E": 99, "F": 99, "G": 99, "H": 99, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 10, "C":  3, "D":  9, "E":  6, "F":  5, "G":  8, "H":  7, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D": 99, "E": 99, "F":  3, "G": 99, "H":  4, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  5, "D":  8, "E":  7, "F":  6, "G":  9, "H":  4, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  3, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  7, "D":  6, "E":  8, "F":  4, "G":  9, "H":  5, "I": 10, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  4, "C": 99, "D":  3, "E": 99, "F": 99, "G":  5, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  5, "D":  3, "E":  4, "F": 99, "G":  6, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  6, "D": 10, "E":  5, "F":  4, "G":  7, "H":  8, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B":  4, "C":  7, "D":  8, "E":  5, "F":  9, "G": 10, "H":  3, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  5, "E":  3, "F": 99, "G":  4, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  4, "D": 99, "E":  1, "F": 99, "G": 99, "H": 99, "I":  3, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  1, "F": 99, "G": 99, "H":  3, "I":  4, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  1, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  1, "F": 99, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C":  3, "D": 99, "E":  1, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C":  5, "D":  3, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C":  2, "D":  4, "E": 99, "F":  3, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G":  1, "H":  4, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  3, "D":  2, "E":  4, "F":  5, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  5, "C": 99, "D": 99, "E": 99, "F":  4, "G":  1, "H":  6, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C":  6, "D":  4, "E":  2, "F": 99, "G":  1, "H": 99, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C":  2, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  6, "B":  3, "C":  7, "D":  2, "E":  4, "F": 10, "G":  1, "H":  8, "I":  9, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C":  5, "D": 99, "E": 99, "F":  2, "G":  1, "H": 99, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C": 99, "D":  4, "E": 99, "F": 99, "G":  1, "H":  2, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  8, "B":  9, "C":  7, "D":  2, "E":  3, "F":  4, "G":  1, "H": 10, "I":  5, "J":  6}},
            { "count":1, "ballot":{"A":  2, "B":  3, "C":  5, "D":  6, "E":  9, "F": 10, "G":  1, "H":  4, "I":  8, "J":  7}},
            { "count":1, "ballot":{"A":  2, "B":  7, "C":  3, "D":  4, "E":  9, "F":  8, "G":  1, "H": 10, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C":  9, "D":  3, "E":  8, "F": 10, "G":  1, "H":  7, "I":  2, "J":  6}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  1, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  2, "B": 99, "C": 99, "D":  4, "E":  3, "F": 99, "G":  1, "H":  6, "I":  7, "J":  5}},
            { "count":1, "ballot":{"A":  4, "B":  9, "C":  7, "D": 10, "E":  3, "F":  2, "G":  1, "H":  8, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A":  9, "B":  8, "C":  7, "D":  2, "E": 10, "F":  6, "G":  1, "H":  5, "I":  4, "J":  3}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I":  3, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H":  3, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E":  4, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C":  8, "D":  7, "E": 10, "F":  9, "G":  2, "H":  6, "I":  5, "J":  1}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I":  4, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D":  3, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  8, "C":  7, "D":  3, "E": 10, "F":  4, "G":  2, "H":  9, "I":  6, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D":  3, "E":  4, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D":  3, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D": 99, "E": 99, "F":  3, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A":  4, "B":  3, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  3, "C": 99, "D":  4, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  3, "H": 99, "I":  2, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  4, "F": 99, "G":  2, "H":  3, "I":  1, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  7, "C":  8, "D": 10, "E":  9, "F":  6, "G":  4, "H":  2, "I":  5, "J":  1}},
            { "count":1, "ballot":{"A":  5, "B":  9, "C": 10, "D":  6, "E":  8, "F":  4, "G":  3, "H":  2, "I":  7, "J":  1}},
            { "count":1, "ballot":{"A":  7, "B":  4, "C":  2, "D":  6, "E":  8, "F":  5, "G":  3, "H": 10, "I":  9, "J":  1}},
            { "count":1, "ballot":{"A": 99, "B":  4, "C": 99, "D": 99, "E":  3, "F":  1, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  7, "C":  6, "D": 10, "E":  9, "F":  1, "G":  2, "H":  4, "I":  8, "J":  5}},
            { "count":1, "ballot":{"A":  3, "B":  4, "C": 99, "D": 99, "E": 99, "F":  1, "G":  2, "H": 99, "I": 99, "J":  5}},
            { "count":1, "ballot":{"A":  4, "B":  2, "C": 99, "D": 99, "E": 99, "F":  1, "G": 99, "H":  3, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  5, "B":  6, "C":  7, "D": 10, "E":  8, "F":  1, "G":  2, "H":  3, "I":  9, "J":  4}},
            { "count":1, "ballot":{"A":  4, "B":  3, "C":  5, "D":  9, "E":  8, "F":  1, "G":  6, "H": 10, "I":  7, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B":  8, "C":  5, "D":  9, "E":  7, "F":  1, "G":  3, "H": 99, "I":  2, "J":  6}},
            { "count":1, "ballot":{"A":  2, "B":  4, "C":  3, "D":  5, "E":  6, "F":  1, "G": 10, "H":  8, "I":  9, "J":  7}},
            { "count":1, "ballot":{"A":  5, "B":  9, "C":  2, "D": 10, "E":  3, "F":  1, "G":  6, "H":  7, "I":  4, "J":  8}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C": 99, "D": 99, "E": 99, "F":  1, "G":  3, "H": 99, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  6, "B":  7, "C": 10, "D":  9, "E":  5, "F":  1, "G":  2, "H":  9, "I":  4, "J":  3}},
            { "count":1, "ballot":{"A":  3, "B":  2, "C": 99, "D":  4, "E": 99, "F":  1, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  5, "B":  6, "C":  4, "D": 10, "E":  3, "F":  1, "G":  2, "H":  7, "I":  9, "J":  8}},
            { "count":1, "ballot":{"A":  5, "B":  4, "C":  7, "D":  8, "E":  1, "F":  3, "G":  6, "H":  9, "I": 10, "J":  2}},
            { "count":1, "ballot":{"A":  2, "B":  5, "C": 99, "D": 99, "E":  1, "F":  4, "G": 99, "H": 99, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B":  6, "C":  7, "D":  9, "E":  1, "F":  2, "G":  8, "H":  5, "I":  4, "J": 10}},
            { "count":1, "ballot":{"A": 99, "B":  2, "C":  5, "D": 99, "E":  3, "F":  1, "G":  4, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C":  3, "D": 99, "E": 99, "F":  1, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C": 99, "D": 99, "E":  2, "F":  1, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  3, "D": 99, "E": 99, "F":  1, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  3, "D": 99, "E": 99, "F":  1, "G":  4, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F":  1, "G":  3, "H":  4, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  5, "D": 99, "E": 99, "F":  1, "G": 99, "H":  3, "I":  4, "J":  2}},
            { "count":1, "ballot":{"A":  5, "B": 99, "C":  3, "D": 99, "E": 99, "F":  1, "G":  4, "H": 99, "I":  6, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  2, "F":  1, "G":  5, "H": 99, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  4, "B": 99, "C":  5, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I":  1, "J":  3}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E":  1, "F":  2, "G":  3, "H": 99, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  1, "D": 99, "E":  2, "F":  3, "G": 99, "H":  4, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  2, "D": 99, "E":  1, "F":  3, "G": 99, "H":  4, "I": 99, "J":  5}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  4, "D": 99, "E":  3, "F":  1, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  3, "B": 99, "C": 99, "D": 99, "E": 99, "F":  1, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C": 99, "D": 99, "E": 99, "F":  1, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A": 99, "B": 99, "C":  2, "D": 99, "E": 99, "F":  1, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  7, "C":  5, "D":  2, "E": 10, "F":  8, "G":  6, "H":  9, "I":  3, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  3, "D": 99, "E": 99, "F": 99, "G":  2, "H":  4, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  6, "C":  8, "D":  2, "E":  9, "F":  5, "G":  7, "H":  4, "I": 10, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B":  4, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H":  2, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  5, "E":  4, "F": 99, "G": 99, "H": 99, "I":  3, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  4, "D":  5, "E": 99, "F":  6, "G":  3, "H":  7, "I":  8, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  5, "D":  3, "E":  4, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B": 10, "C":  9, "D":  8, "E":  6, "F":  4, "G":  7, "H":  2, "I":  5, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  3, "D":  2, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C": 99, "D": 99, "E":  2, "F":  4, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B": 10, "C":  6, "D":  4, "E":  9, "F":  8, "G":  3, "H":  7, "I":  2, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  2, "D": 99, "E": 99, "F": 99, "G": 99, "H":  3, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  4, "C": 99, "D": 99, "E": 99, "F":  3, "G":  2, "H": 99, "I": 99, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I":  4, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  4, "E": 99, "F":  5, "G":  3, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  7, "C":  4, "D":  7, "E":  8, "F":  9, "G":  3, "H":  5, "I":  6, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  3, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  6, "C":  3, "D":  7, "E":  2, "F":  9, "G":  5, "H":  4, "I": 10, "J":  8}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  2, "D":  7, "E":  8, "F":  9, "G":  3, "H":  4, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  2, "E": 99, "F": 99, "G":  3, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B": 10, "C":  9, "D":  2, "E":  5, "F":  3, "G":  7, "H":  6, "I":  8, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H":  4, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B":  6, "C": 99, "D": 99, "E":  3, "F": 99, "G": 99, "H":  4, "I":  5, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  8, "C":  9, "D":  4, "E":  7, "F":  2, "G":  3, "H": 10, "I":  6, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B":  6, "C": 10, "D":  3, "E":  9, "F":  7, "G":  8, "H":  2, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  4, "G":  3, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  9, "C":  2, "D":  8, "E":  3, "F": 10, "G":  4, "H":  6, "I":  7, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B":  4, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H":  3, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  3, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  3, "D": 99, "E": 99, "F":  2, "G": 99, "H": 99, "I":  5, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  2, "D":  3, "E":  5, "F": 99, "G":  4, "H": 99, "I": 99, "J":  6}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G":  3, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  4, "C": 10, "D":  6, "E":  5, "F":  8, "G":  2, "H":  9, "I":  3, "J":  7}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  3, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H":  4, "I":  3, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  6, "C":  2, "D":  5, "E":  3, "F":  9, "G": 10, "H":  7, "I":  4, "J":  8}},
            { "count":1, "ballot":{"A":  1, "B":  8, "C":  9, "D":  2, "E":  4, "F":  7, "G": 10, "H":  5, "I":  6, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F": 99, "G":  2, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C": 99, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I":  5, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B":  7, "C":  8, "D":  9, "E":  6, "F":  4, "G": 10, "H":  3, "I":  5, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C": 99, "D": 99, "E": 99, "F":  5, "G": 99, "H":  4, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  2, "D":  4, "E":  3, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A": 99, "B":  1, "C": 99, "D": 99, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  4, "C": 99, "D":  5, "E": 99, "F":  3, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  6, "D":  9, "E":  5, "F":  7, "G":  8, "H":  3, "I": 10, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  2, "C":  3, "D": 99, "E": 99, "F": 99, "G":  4, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C": 99, "D":  4, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  2, "E":  3, "F": 99, "G": 99, "H": 99, "I": 99, "J":  4}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C":  2, "D":  8, "E":  7, "F": 10, "G":  9, "H":  6, "I":  4, "J":  5}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D":  3, "E": 99, "F":  4, "G": 99, "H": 99, "I": 99, "J":  2}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C": 99, "D": 99, "E": 99, "F":  2, "G": 99, "H":  4, "I": 99, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B":  6, "C": 10, "D":  2, "E":  5, "F":  8, "G":  3, "H":  9, "I":  4, "J":  7}},
            { "count":1, "ballot":{"A":  1, "B":  4, "C": 10, "D":  5, "E":  9, "F":  8, "G":  6, "H":  2, "I":  7, "J":  3}},
            { "count":1, "ballot":{"A":  1, "B": 99, "C":  3, "D":  2, "E": 99, "F": 99, "G": 99, "H": 99, "I": 99, "J": 99}},
            { "count":1, "ballot":{"A":  1, "B":  3, "C":  7, "D":  2, "E": 10, "F":  8, "G":  6, "H":  9, "I":  4, "J":  5}}
        ]
        
        output = SchulzeSTV.__proportionalCompletion__("H", set(["A","C","D","I"]), input)
        self.assertEqual(output, {
            (1, 1, 1, 1): 115.90588590649332,
            (1, 1, 1, 3): 22.199966129399414,
            (1, 1, 3, 1): 29.879239775715977,
            (1, 1, 3, 3): 16.617881161364277,
            (1, 3, 1, 1): 53.964692432194951,
            (1, 3, 1, 3): 27.040269035296657,
            (1, 3, 3, 1): 33.326877436337327,
            (1, 3, 3, 3): 50.416539474549459,
            (3, 1, 1, 1): 3.8361852711905304,
            (3, 1, 1, 3): 5.8472929109852849,
            (3, 1, 3, 1): 7.1392081267534939,
            (3, 1, 3, 3): 8.4493407180977176,
            (3, 3, 1, 1): 5.2051766103125825,
            (3, 3, 1, 3): 6.7481952555291649,
            (3, 3, 3, 1): 15.275312344684572,
            (3, 3, 3, 3): 58.147937411095306
        })
        
    # Schulze STV, example from Markus' part 3 of 5: Implementing the Schulze
    # STV Method. See calcul02.pdf (Abstract: In this paper we illustrate the
    # calculation of the strengths of the vote managements.) 
    def testSchulzeSTVVoteManagementStrengthCalculation(self):
        
        # Generate data
        input = [
            (36.597383, 1,1,1,1),
            (5.481150,  1,1,1,3),
            (13.27913,  1,1,3,1),
            (4.859413,  1,1,3,3),
            (35.425375, 1,3,1,1),
            (5.490934,  1,3,1,3),
            (22.855333, 1,3,3,1),
            (19.835570, 1,3,3,3),
            (22.928716, 3,1,1,1),
            (5.538309,  3,1,1,3),
            (13.130227, 3,1,3,1),
            (6.056291,  3,1,3,3),
            (23.992772, 3,3,1,1),
            (16.699207, 3,3,1,3),
            (98.165759, 3,3,3,1),
            (129.66443, 3,3,3,3)
        ]
        output = SchulzeSTV.__strengthOfVoteManagement__(input)
        
        # Run tests
        self.assertAlmostEqual(output, 77.3899369763)


if __name__ == "__main__":
    unittest.main()