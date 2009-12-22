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

from plurality import Plurality
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


if __name__ == "__main__":
    unittest.main()