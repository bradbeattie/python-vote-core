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

from pyvotecore.tie_breaker import TieBreaker
import unittest


class TestTieBreaker(unittest.TestCase):

    def setUp(self):
        self.tieBreaker = TieBreaker(['a', 'b', 'c', 'd'])
        self.tieBreaker.random_ordering = ['a', 'b', 'c', 'd']

    def test_simple_tie(self):
        self.assertEqual(
            self.tieBreaker.break_ties(set(['b', 'c'])),
            'b'
        )

    def test_simple_tie_reverse(self):
        self.assertEqual(
            self.tieBreaker.break_ties(set(['b', 'c']), reverse=True),
            'c'
        )

    def test_tuple_tie(self):
        self.assertEqual(
            self.tieBreaker.break_ties(set([('c', 'a'), ('b', 'd'), ('c', 'b')])),
            ('b', 'd')
        )

    def test_tuple_tie_reverse(self):
        self.assertEqual(
            self.tieBreaker.break_ties(set([('c', 'a'), ('b', 'd'), ('c', 'b')]), reverse=True),
            ('c', 'b')
        )

if __name__ == "__main__":
    unittest.main()
