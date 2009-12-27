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

from plurality_at_large import PluralityAtLarge
import unittest

class TestPluralityAtLarge(unittest.TestCase):
    
    
    # Plurality, no ties
    def testPluralityNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":22, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]
        output = PluralityAtLarge.calculate_winner(input)
        
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
        output = PluralityAtLarge.calculate_winner(input)
        
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
        output = PluralityAtLarge.calculate_winner(input)

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
        output = PluralityAtLarge.calculate_winner(input)
        
        # Run tests
        self.assertEqual(output["tallies"], {'c1':26, 'c2':26, 'c3':23})
        self.assertEqual(output["tied_winners"], set(['c1', 'c2']))
        self.assert_(list(output["winners"])[0] in output["tied_winners"])
        self.assertEqual(len(output["tie_breaker"]), 3)

    
    # Plurality at Large, no ties
    def testPluralityAtLargeNoTies(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":["c1", "c2"] },
            { "count":22, "ballot":["c1", "c3"] },
            { "count":23, "ballot":["c2", "c3"] }
        ]
        output = PluralityAtLarge.calculate_winner(input, 2)
        
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
        output = PluralityAtLarge.calculate_winner(input, 2)
        
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
        output = PluralityAtLarge.calculate_winner(input, 2)

        # Run tests
        self.assertEqual(output["tallies"], {'c3': 52, 'c2': 52, 'c1': 56, 'c4': 12})
        self.assertEqual(len(output["tie_breaker"]), 4)
        self.assertEqual(output["tied_winners"], set(['c2','c3']))
        self.assert_("c1" in output["winners"] and ("c2" in output["winners"] or "c3" in output["winners"]))
        self.assertEqual(len(output), 4)


if __name__ == "__main__":
    unittest.main()
