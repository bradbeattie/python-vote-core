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

from pyvotecore.schulze_pr import SchulzePR
import time
import unittest


class TestSchulzePR(unittest.TestCase):

    def test_10_candidates_5_winners(self):
        """
        This test considers a case that SchulzeSTV starts to choke on due to
        the potential number of nodes and edges to consider.
        """

        # Generate data
        startTime = time.time()
        input = [
            {"count": 1, "ballot": {"A": 9, "B": 1, "C": 1, "D": 9, "E": 9,
                                    "F": 2, "G": 9, "H": 9, "I": 9, "J": 9}},
            {"count": 1, "ballot": {"A": 3, "B": 2, "C": 3, "D": 1, "E": 9,
                                    "F": 9, "G": 9, "H": 9, "I": 9, "J": 9}},
            {"count": 1, "ballot": {"A": 9, "B": 9, "C": 9, "D": 9, "E": 1,
                                    "F": 9, "G": 9, "H": 9, "I": 9, "J": 9}}
        ]
        SchulzePR(input, winner_threshold=5,
                  ballot_notation="ranking").as_dict()

        # Run tests
        self.assert_(time.time() - startTime < 1)

    def test_10_candidates_9_winners(self):
        """
        This test considers a case that SchulzeSTV starts to choke on due to
        the potential size of the completion patterns
        """

        # Generate data
        startTime = time.time()
        input = [
            {"count": 1, "ballot": {"A": 9, "B": 1, "C": 1, "D": 9, "E": 9,
                                    "F": 2, "G": 9, "H": 9, "I": 9, "J": 9}},
            {"count": 1, "ballot": {"A": 3, "B": 2, "C": 3, "D": 1, "E": 9,
                                    "F": 9, "G": 9, "H": 9, "I": 9, "J": 9}},
            {"count": 1, "ballot": {"A": 9, "B": 9, "C": 9, "D": 9, "E": 1,
                                    "F": 9, "G": 9, "H": 9, "I": 9, "J": 9}}
        ]
        SchulzePR(input, winner_threshold=9,
                  ballot_notation="ranking").as_dict()

        # Run tests
        self.assert_(time.time() - startTime < 2)

if __name__ == "__main__":
    unittest.main()
