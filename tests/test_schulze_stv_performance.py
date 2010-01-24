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
import unittest, time

class TestSchulzeSTV(unittest.TestCase):

    # This test considers a case in which there are 10 choose 5 (252) possible
    # outcomes and 252 choose 2 (31626) possible edges between them.
    def test_10_candidates_5_winners(self):
        
        # Generate data
        startTime = time.time()
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9, "G":9, "H":9, "I":9, "J":9 }}
        ]
        SchulzeSTV.calculate_winner(input, 5, "ranking")
        
        # Run tests
        self.assert_(time.time() - startTime < 2)
        
    # This test looks at few graph notes, but large completion patterns. With
    # 10 candidates and 9 winners, we're looking at 3^9 (19683) patterns to
    # consider.
    def test_10_candidates_9_winners(self):
        
        # Generate data
        startTime = time.time()
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9, "G":9, "H":9, "I":9, "J":9 }}
        ]
        SchulzeSTV.calculate_winner(input, 9, "ranking")
        
        # Run tests
        self.assert_(time.time() - startTime < 2)
        
    # This test ensures that if you request the same number of winners as there
    # are candidates, the system doesn't take the long route to calculate them.
    def test_10_candidates_10_winners(self):
        
        # Generate data
        startTime = time.time()
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9, "G":9, "H":9, "I":9, "J":9 }}
        ]
        output = SchulzeSTV.calculate_winner(input, 10, "ranking")
        
        # Run tests
        self.assertAlmostEqual(startTime, time.time(), 1)
        self.assertEqual(output, {
            'winners': set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J']),
            'candidates': set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J'])
        })

if __name__ == "__main__":
    unittest.main()
