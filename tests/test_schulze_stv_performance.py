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

    # This test ensures that complex calculations take under a certain threshold
    # of time. As the algorithm is improved, we might want to tighten this test
    # from two seconds down to something lower.
    def test_10_candidates_5_winners(self):
        startTime = time.time()
        
        # Generate data
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9, "G":9, "H":9, "I":9, "J":9 }}
        ]
        SchulzeSTV.calculate_winner(input, 5, "ranking")
        
        # Run tests
        print time.time() - startTime
        self.assert_(time.time() - startTime < 2)
        
    # This test ensures that complex calculations take under a certain threshold
    # of time. As the algorithm is improved, we might want to tighten this test
    # from two seconds down to something lower.
    def test_10_candidates_9_winners(self):
        return
    
        startTime = time.time()
        
        # Generate data
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9, "G":9, "H":9, "I":9, "J":9 }}
        ]
        SchulzeSTV.calculate_winner(input, 9, "ranking")
        
        # Run tests
        print time.time() - startTime
        self.assert_(time.time() - startTime < 2)
        
    # This test ensures that complex calculations take under a certain threshold
    # of time. As the algorithm is improved, we might want to tighten this test
    # from two seconds down to something lower.
    def test_10_candidates_10_winners(self):
        return
    
        startTime = time.time()
        
        # Generate data
        input = [
            { "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9, "G":9, "H":9, "I":9, "J":9 }},
            { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9, "G":9, "H":9, "I":9, "J":9 }}
        ]
        SchulzeSTV.calculate_winner(input, 10, "ranking")
        
        # Run tests
        print time.time() - startTime
        self.assert_(time.time() - startTime < 2)

if __name__ == "__main__":
    unittest.main()
