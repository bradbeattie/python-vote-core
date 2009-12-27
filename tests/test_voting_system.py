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

from voting_system import VotingSystem
import unittest

class TestVotingSystem(unittest.TestCase):
    
    # Tie breaker generation
    def test_tieBreakerGeneration(self):
        
        # Generate data
        input = [
            { "count":26, "ballot":"c1" },
            { "count":22, "ballot":"c2" },
            { "count":23, "ballot":"c3" }
        ]

if __name__ == "__main__":
    unittest.main()
