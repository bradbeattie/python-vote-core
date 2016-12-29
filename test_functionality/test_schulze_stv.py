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

from pyvotecore.schulze_stv import SchulzeSTV
from pyvotecore.schulze_helper import SchulzeHelper
import unittest


class TestSchulzeSTV(unittest.TestCase):

    # This example was detailed in Markus Schulze's schulze2.pdf (Free Riding
    # and Vote Management under Proportional Representation by the Single
    # Transferable Vote, section 5.5).
    def test_part_2_of_5_example(self):

        # Generate data
        input = [
            {"count": 60, "ballot": [["a"], ["b"], ["c"], ["d"], ["e"]]},
            {"count": 45, "ballot": [["a"], ["c"], ["e"], ["b"], ["d"]]},
            {"count": 30, "ballot": [["a"], ["d"], ["b"], ["e"], ["c"]]},
            {"count": 15, "ballot": [["a"], ["e"], ["d"], ["c"], ["b"]]},
            {"count": 12, "ballot": [["b"], ["a"], ["e"], ["d"], ["c"]]},
            {"count": 48, "ballot": [["b"], ["c"], ["d"], ["e"], ["a"]]},
            {"count": 39, "ballot": [["b"], ["d"], ["a"], ["c"], ["e"]]},
            {"count": 21, "ballot": [["b"], ["e"], ["c"], ["a"], ["d"]]},
            {"count": 27, "ballot": [["c"], ["a"], ["d"], ["b"], ["e"]]},
            {"count": 9, "ballot": [["c"], ["b"], ["a"], ["e"], ["d"]]},
            {"count": 51, "ballot": [["c"], ["d"], ["e"], ["a"], ["b"]]},
            {"count": 33, "ballot": [["c"], ["e"], ["b"], ["d"], ["a"]]},
            {"count": 42, "ballot": [["d"], ["a"], ["c"], ["e"], ["b"]]},
            {"count": 18, "ballot": [["d"], ["b"], ["e"], ["c"], ["a"]]},
            {"count": 6, "ballot": [["d"], ["c"], ["b"], ["a"], ["e"]]},
            {"count": 54, "ballot": [["d"], ["e"], ["a"], ["b"], ["c"]]},
            {"count": 57, "ballot": [["e"], ["a"], ["b"], ["c"], ["d"]]},
            {"count": 36, "ballot": [["e"], ["b"], ["d"], ["a"], ["c"]]},
            {"count": 24, "ballot": [["e"], ["c"], ["a"], ["d"], ["b"]]},
            {"count": 3, "ballot": [["e"], ["d"], ["c"], ["b"], ["a"]]},
        ]
        output = SchulzeSTV(input, required_winners=3, ballot_notation=SchulzeSTV.BALLOT_NOTATION_GROUPING).as_dict()

        # Run tests
        self.assertEqual(output['winners'], set(['a', 'd', 'e']))

    # http://en.wikipedia.org/wiki/Schulze_STV#Count_under_Schulze_STV
    def test_wiki_example_1(self):

        # Generate data
        input = [
            {"count": 12, "ballot": [["Andrea"], ["Brad"], ["Carter"]]},
            {"count": 26, "ballot": [["Andrea"], ["Carter"], ["Brad"]]},
            {"count": 12, "ballot": [["Andrea"], ["Carter"], ["Brad"]]},
            {"count": 13, "ballot": [["Carter"], ["Andrea"], ["Brad"]]},
            {"count": 27, "ballot": [["Brad"]]},
        ]
        output = SchulzeSTV(input, required_winners=2, ballot_notation=SchulzeSTV.BALLOT_NOTATION_GROUPING).as_dict()

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
            {"count": 12, "ballot": [["Andrea"], ["Brad"], ["Carter"]]},
            {"count": 26, "ballot": [["Andrea"], ["Carter"], ["Brad"]]},
            {"count": 12, "ballot": [["Carter"], ["Andrea"], ["Brad"]]},
            {"count": 13, "ballot": [["Carter"], ["Andrea"], ["Brad"]]},
            {"count": 27, "ballot": [["Brad"]]},
        ]
        output = SchulzeSTV(input, required_winners=2, ballot_notation=SchulzeSTV.BALLOT_NOTATION_GROUPING).as_dict()

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
            {"count": 1, "ballot": {"a": 1, "b": 1, "c": 3}}
        ]
        output = SchulzeSTV(input, required_winners=1, ballot_notation=SchulzeSTV.BALLOT_NOTATION_RATING).as_dict()

        # Run tests
        self.assertEqual(output['winners'], set(["c"]))

    # This example ensures that vote management strength calculations are
    # calculated correctly.
    def test_one_ballot_two_winners(self):

        # Generate data
        input = [
            {"count": 1, "ballot": {"Metal": 1, "Paper": 1, "Plastic": 2, "Wood": 2}},
        ]
        output = SchulzeSTV(input, required_winners=2, ballot_notation=SchulzeSTV.BALLOT_NOTATION_RANKING).as_dict()

        # Run tests
        self.assertEqual(output, {
            'candidates': set(['Paper', 'Wood', 'Metal', 'Plastic']),
            'winners': set(['Paper', 'Metal'])
        })

    # This example ensures that the proportional completion round correctly
    # accounts for sparse pattern weights.
    def test_two_ballots_two_winners(self):

        # Generate data
        input = [
            {"count": 1, "ballot": {"Metal": 2, "Paper": 1, "Plastic": 2, "Wood": 2}},
            {"count": 1, "ballot": {"Metal": 2, "Paper": 2, "Plastic": 2, "Wood": 1}}
        ]
        output = SchulzeSTV(input, required_winners=2, ballot_notation=SchulzeSTV.BALLOT_NOTATION_RANKING).as_dict()

        # Run tests
        self.assertEqual(output, {
            "candidates": set(['Metal', 'Wood', 'Plastic', 'Paper']),
            "winners": set(['Paper', 'Wood']),
        })

    #
    def test_happenstance_example(self):

        # Generate data
        input = [
            {"count": 1, "ballot": {"A": 9, "B": 1, "C": 1, "D": 9, "E": 9, "F": 2}},
            {"count": 1, "ballot": {"A": 3, "B": 2, "C": 3, "D": 1, "E": 9, "F": 9}},
            {"count": 1, "ballot": {"A": 9, "B": 9, "C": 9, "D": 9, "E": 1, "F": 9}}
        ]
        output = SchulzeSTV(input, required_winners=2, ballot_notation=SchulzeSTV.BALLOT_NOTATION_RANKING).as_dict()

        # Run tests
        self.assertEqual(
            output["tied_winners"],
            set([('D', 'E'), ('B', 'E'), ('C', 'E'), ('B', 'D')])
        )

    # Any winner set should include one from each of A, B, and C
    def test_happenstance_example_2(self):

        # Generate data
        input = [
            {"count": 5, "ballot": [["A1", "A2"], ["B1", "B2"], ["C1", "C2"]]},
            {"count": 2, "ballot": [["B1", "B2"], ["A1", "A2", "C1", "C2"]]},
            {"count": 4, "ballot": [["C1", "C2"], ["B1", "B2"], ["A1", "A2"]]},
        ]
        output = SchulzeSTV(input, required_winners=3, ballot_notation=SchulzeSTV.BALLOT_NOTATION_GROUPING).as_dict()

        # Run tests
        self.assertTrue(set(["A1", "A2"]) & output["winners"])
        self.assertTrue(set(["B1", "B2"]) & output["winners"])
        self.assertTrue(set(["C1", "C2"]) & output["winners"])

    # Proportional completion example worked through in Schulze's calcul01.pdf
    def test_A53_proportional_completion(self):

        # From A53.dat
        A53 = '''\
  1  1 99 99 99 99  4  3  2 99 99
  2  1  2  4  5  3  9  6 10  8  7
  3  2  6 10  7  3  8  5  9  1  4
  4 99 99 99 99 99 99 99 99 99  1
  5 99 99 99 99 99 99 99 99 99  1
  6  3 99 99 99  5  4  6  7  2  1
  7  4 99  3 99 99 99 99 99  2  1
  8  3 99  1 99 99 99 99 99  4  2
  9  2 99  1 99 99 99 99 99 99 99
 10  3 99 99 99 99 99 99  2 99  1
 11 99  5 99 99  1  4  2 99  3  6
 12 99  4  5 99  1 99  2  3 99 99
 13  7  9  6 10  1  5  3  4  8  2
 14  4  5  3  9  1 10  2  6  8  7
 15 99 99 99 99  2 99  3 99  1  4
 16 99 99  4 99  2 99  3 99  1 99
 17  2 99  5 99  1 99  4 99  6  3
 18 99 99 99 99  1  4  2 99 99  3
 19  3 99 99  6 99  4  5  1 99  2
 20  4 99 99  5 99  2  3 99 99  1
 21  4  9  7  5  8  2 10  6  3  1
 22  4  7  3  6  8  2 10  5  9  1
 23  4 99 99  6  3  2 99  5 99  1
 24 99  5 99  4 99  3 99 99  2  1
 25 99 99 99  4 99  3 99 99  2  1
 26  4 10  9  8  7  3  5  6  2  1
 27  4 99 99  6 99  3 99  5  2  1
 28  3  4 99  2 99 99 99  5 99  1
 29  3 99 99  2 99 99 99 99 99  1
 30  8  9  7  2  3  4  5  6 10  1
 31  5  7  6  2  3  4 10  9  8  1
 32 10  8  4  2  3  9  7  5  6  1
 33  4  6 99  2  5  3 99 99 99  1
 34 99 99 99  2 99 99  3 99 99  1
 35  3  9  7  2  4  8  6 10  5  1
 36  1  5  2 99 99 99  3 99 99  4
 37  1  7  5  3  9  6  8  4 10  2
 38  1  7  5  6  3  2  8  9 10  4
 39  1  2  4  3 10  9  5  8  7  6
 40  1 99 99  3  6  2 99  4 99  5
 41  1 99 99 99 99 99  2 99 99 99
 42  1  8  5  2  4  3 10  9  7  6
 43  1 99 99  2  3  5 99 99  4 99
 44  1  2  3  5  7  4  8  9 10  6
 45  1  2  7  4  6  5  9 10  8  3
 46  1  2  3  5  4  6 10 11 12  7
 47  1  3  8  7  6  5  4  2  9 10
 48  1  7  6  4  5  2  8 10  9  3
 49  1  3  7  6 10  4  9  5  8  2
 50  1  8 10  4  7  2  3  9  6  5
 51  1 99  6 99  2  3 99  7  5 99
 52  1  3  6 10  7  9  5  2  8  4
 53  1 10  4  9  7  2  5  8  3  6
 54  1 99 99 99 99  2 99  3 99  4
 55  1  2 99 99 99 99  3 99 99  4
 56  4  5 99 99  6 99 99  3  2  1
 57  4  5  6 10  8  9  7  3  2  1
 58  4  5  9  6  7  8 10  2  3  1
 59  6  3  5  7 10  4  8  2  9  1
 60 10  3  4  9  5  6  8  2  7  1
 61  3  4  2  7  8  9 10  5  6  1
 62  7  3  6  9  2  8  5 10  4  1
 63  4  3  7  9  2  6 10  5  8  1
 64  5  3 10  7  2  9  8  6  4  1
 65 99  1  2 99 99 99 99 99 99  3
 66 99 99  1  6  2 99  3 99  4  5
 67 99 99  4  3  1 99  2 99 99 99
 68  2  9  8  5  1  6  3  7 10  4
 69  6  3  7  9  2  8  1 10  4  5
 70  4  9  6 10  3  7  1  8  5  2
 71  3  9  5  6  4  8  1  7 10  2
 72  2 99 99 99 99 99  1  4 99  3
 73  7  4  8  5  9  6  1  2 10  3
 74  9 10  8  5  7  6  1  2  3  4
 75 99 99 99  2  3 99  1 99 99 99
 76  7  8 10  3  2  6  1  9  4  5
 77  4  3  2 99 99 99  1 99 99 99
 78  3  7  4  5  6  8  1  9 10  2
 79  5 10  6  7  2  8  1  9  3  4
 80  2  5  4  6  7 10  1  8  9  3
 81 99 99 99 99 99 99  1 99 99  2
 82 99 99 99  3 99 99  1  2 99 99
 83  2  4  3  9 10  8  1  5  7  6
 84  4  7  2  6  5  8  1  9 10  3
 85 99  2 99 99  3 99  1 99 99 99
 86  2  5 99 99  4 99  1 99 99  3
 87  5 99 99  2  4 99  1  3 99  6
 88 99 99 99 99 99 99  1 99  2 99
 89  2 99  4 99 99 99  1 99 99  3
 90  7  3  4  2  9  6  1  8 10  5
 91  2  8  5  7  6  3  1 10  9  4
 92  7 10  6  9  5  4  1  8  3  2
 93 99  2 99 99 99 99  1  3 99 99
 94  3 99 99  2 99 99  1 99 99 99
 95 99 99 99 99 99  3  1 99  2  4
 96 99 99 99  2 99  3  1  4 99 99
 97 99 99 99 99 99  2  1 99  3  4
 98  6 10  8  9  7  5  1  4  2  3
 99  3 99 99  2 99 99  1 99 99 99
100  5 99 99  4 99 99  1  3 99  2
101  4 99 99  3  5 99  1 99 99  2
102  3 99 99 99 99  2  1 99  5  4
103  4  3 99  2 99 99  1 99  5  6
104  3 99 99  4 99  2  1 99  6  5
105 99  4 99  2 99  3  1 99 99 99
106  3 99  4 99  5 99  1  6 99  2
107 10  5  3  2  4  9  1  7  8  6
108  3 99 99  1 99 99 99 99 99  2
109 99  3  2  1 99  4 99 99 99 99
110  2 99 99  1 99 99 99 99  4  3
111 99 99 99  1 99 99 99 99 99  2
112  5  4 99  1 99 99 99  3 99  2
113 99 99 99  1 99 99  2 99 99 99
114  6  5 10  1  3  7  2  8  9  4
115 99 99 99  1  4 99 99 99  3  2
116  2 99 99  1 99 99 99 99 99  3
117 99  4 99  1 99  3 99 99 99  2
118  4  3 99  1 99 99  2 99 99 99
119  2  5  6  1  3  4  7 10  9  8
120 99 99 99  1 99 99  2 99 99 99
121  2 99 99  1 99  3 99 99 99  4
122 99 99 99  1 99 99  2 99 99  3
123  3  4 99  1 99 99  2 99 99 99
124 99 99 99  1 99 99 99 99 99 99
125 99 99 99  1 99  2  4 99  3 99
126 99 99 99  1 99 99 99 99 99 99
127  4  5  7  1  2  9  6  8  3 10
128  3 99 99  1 99 99 99  2 99  4
129  2  3 99  1 99 99  5 99 99  4
130  3 10  6  1  4  8  7  9  5  2
131  2 99  4  1 99  5 99 99 99  3
132 99 99 99  1 99 99 99  3 99  2
133 99 99 99  1  2  3 99 99 99  4
134  3  2  7  1  6  9 10  5  8  4
135  2  5  6  1 99  3  4 99 99 99
136  5  4  8  1  6  9  7  3  2 10
137  2  9  5  1  3 10  8  6  4  7
138 99 99 99  1 99  2 99  3 99  4
139 99 99 99  1  2  3 99 99 99 99
140  9  7  8  1  2  6  3 10  5  4
141  3  4  6  1  7  9  2 10  8  5
142  5  6  7  1  2  9  3 10  4  8
143  3  9  6  1 10  4  2  7  8  5
144 99  4 99  1  5  3 99 99  2 99
145 99 99 99  1 99 99 99 99 99 99
146  2  6  9  1  8  5 10  3  7  4
147  2 99  3  1 99 99 99 99  4  5
148 99 99 99  1 99  2 99 99 99  3
149  2 99 99  1  4 99 99 99 99  3
150  3  6  5  2  7 10  8  9  1  4
151  8  6  7  4  5 10  9  3  1  2
152 99 99 99  3 99 99  4  1 99  2
153  7 99  1  3  6  5  4 99 99  2
154 99 99  1  2 99 99 99 99 99 99
155 99  5  2  3 99  4 99 99  1  6
156 99 99  2  3  5 99  4 99  1  6
157  5  4  9  2  1  6  7  8 10  3
158  4 10  5  2  1  6  3  9  8  7
159 99 99 99  2  1 99 99 99 99 99
160  2 99 99  3  1 99  5 99 99  4
161  2  9  7  5  1  8  6  4 10  3
162 99 99  1  3  2  4 99 99 99 99
163  3  8  9  4 10  1  5  2  6  7
164 99 99  6  4  3  1 99  5 99  2
165  2  8  7  3  4  1  5  9 10  6
166  8  6  5  3 10  1  4  7  9  2
167  5 99  6  3 99  1 99  4 99  2
168  6  8  5  7  4  1  9  3 10  2
169  4 99 99  3 99  1 99 99  5  2
170  6  8  7  2  9  1 10  5  4  3
171  2 99 99  3 99  1 99 99  4 99
172  8  9  6  2  4  1  3 10  5  7
173  2 99 99  5  3  1  4 99 99 99
174 99  5 99  3  4  1 99 99 99  2
175  2  6  7  3  5  1  8 10  9  4
176  9 10  3  8  2  1  4  7  5  6
177  4 99 99  2 99  1  3 99 99 99
178  9  6  4  5  2  3 10  8  1  7
179  5 99  4 99 99  3 99  2 99  1
180 99 99  4 99  6  3  5  2 99  1
181  3 99 99 99 99  5  6  2  4  1
182  3 99 99 99 99  4 99  2 99  1
183  4 99 99 99 99  2 99  3 99  1
184 99 99 99 99 99  2  3 99 99  1
185  4 99 99 99 99  2  3 99 99  1
186  3 99 99 99 99  2  4 99 99  1
187  3  4  5  8  7  2  6  9 10  1
188  7  8  9 10  3  6  4  2  5  1
189 99  4 99 99  2  3 99 99 99  1
190  4  9  7 10  2  5  8  3  6  1
191  3  5  8  6 10  2  7  9  4  1
192 10  5  6  9  4  3  7  8  2  1
193  6  4 99  5 99  3 99  7  2  1
194  5  8  6 10  4  3  9  7  2  1
195 99  7 99 99  5  3  4  6  2  1
196  5 10  9  4  6  7  3  8  1  2
197 99 99 99 99  3 99  2 99  1 99
198 99 99 99 99 99  3  2 99  1  4
199 99 99 99 99 99 99  2  1 99 99
200  3  9  1  5 10  6  2  4  8  7
201  2  7  1  5  6  4  3  8  9 10
202  2  6  1  7  9 10  3  8  5  4
203 99  5  1 99 99 99  2  3  4 99
204 99 99  1 99  4 99  3 99  5  2
205  9 10  1  8  7  3  2  5  4  6
206  2 99  3  5 99 99  4  1 99 99
207  4 99 99 99  3 99 99  2 99  1
208  4 99 99 99  3 99 99  2 99  1
209 99 99 99 99  2 99 99 99 99  1
210 99 99 99 99  2 99 99  3  4  1
211  2  6  5  8  3  9  7  1 10  4
212  3 99  4 99 99  2  1 99 99 99
213 99 99 99 99 99 99  1  2  3 99
214 99  4 99 99 99  2  1  3 99 99
215 99 99  5 99  6  4  1 99  3  2
216  5  4  6 99  8  2  1  7 99  3
217  8 10  3  6  7  2  1  4  9  5
218 99 99 99  3 99  2  1 99  4  5
219  3  4  5 10  6  9  1  8  7  2
220  2  6 10  8  7  4  1  5  9  3
221 99  3 99  2 99  4  1 99 99 99
222 99 99 99  3  4 99 99 99  2  1
223  3 99  5  4 99 99 99  2 99  1
224  4 99 99  3 99 99 99  2 99  1
225  3 99  2  4 99 99 99 99 99  1
226  4  9  2  6  5  7  8  3 10  1
227  3  7  4  6  5  9  8  2 10  1
228  5  4 99  3  2 99 99 99 99  1
229  3  1 99 99 99  5  4 99  6  2
230  2  1 99 99 99 99  4 99  3 99
231  2  1 99 99 99  3 99 99  4 99
232 99  1 99 99 99 99  3 99 99  2
233  4  1  2  3 99 99 99 99 99  5
234  6  1  5  7  4  8  2  9 10  3
235  9  1  5 10  4  2  6  8  7  3
236  4  1  5  9  3  6  8  7 10  2
237 99  1 99 99  3 99  2 99 99 99
238  2  1  3 99 99  4  5 99 99 99
239 99  1 99 99  2 99 99  3 99  4
240 99  1 99 99 99 99 99 99 99 99
241  3  1  7  2  8  9  4 10  6  5
242 99  1 99 99  2 99  3  4  5  6
243  2  1  9  6  5  7 10  3  8  4
244  7  1  8  3  6  4  5  9 10  2
245  5  1  6  7  2 10  3  9  8  4
246  2  1  8  5  9  6 10  7  3  4
247  2  1  3 10  4  5  7  6  8  9
248 99  1 99 99  2  4 99  3 99 99
249  6  1  4  8  7  2  5 10  9  3
250  2  1  9 10  7  6  4  5  8  3
251  4  1  5  6 99 99  2  7 99  3
252 99  1 99 99 99  2 99 99  3  4
253 99  1  5 99  2 99  3 99 99  4
254  3  1  5  2  8  4 10  7  9  6
255  6  1  5  7  4  8  3  9  2 10
256  5  1  6  3  2  9  4  7  8 10
257  9  1  6  5  3 10  2  4  7  8
258  6  1  3  5  4 10  2  8  9  7
259 99  1 99 99 99  2 99 99  3  4
260 99  1 99 99  4  3  5 99 99  2
261 99  1  4 99 99  2 99 99 99  3
262 99  1 99 99  2 99 99  3  4 99
263 99  1 99 99 99  4  2 99 99  3
264  5  1  9  4  2  6 10  7  8  3
265  2  1  8  7  6  5  9 10  3  4
266  3  1  7  6  9  5  4  8 10  2
267  9  2  8  3  7 10  4  6  1  5
268 99  3 99  4 99  5 99  1 99  2
269 99  3  2 99  6 99  5  1 99  4
270  7  4  2 10  5  9  6  1  3  8
271  6  4  3 10  5  7  9  1  8  2
272  3  2  1 99 99 99 99 99  4 99
273 99  2  1 99 99  3 99 99 99  4
274  9  5  8  7  2  6 10  1  3  4
275  4  2  8  7  1 10  9  5  3  6
276 99  2 99 99  1 99 99 99 99 99
277  4  5  6  8  3  9 10  1  7  2
278  6  3  5 10  1  4  9  7  8  2
279  2  6  9 10  1  7  8  3  4  5
280  6  4 99 99  3  5 99  1 99  2
281  7  2  8  6  4  9  3 10  5  1
282  3  2 99 99 99 99  4 99 99  1
283  5  2  8  4  3  6 10  7  9  1
284  7  2  9  8  3 10  4  5  6  1
285 99  2 99  3 99 99 99  4 99  1
286  5  2 10  7  4  3  8  6  9  1
287  4  2  6  5  3  8  7 10  9  1
288  2  3  9  5 10  6  7  4  8  1
289  2  4 99  6  3 99 99  5 99  1
290  2  4 99 99  5  6  3 99 99  1
291  2  3 99 99 99 99  5  4 99  1
292  2  3 10  4  9  5  6  7  8  1
293  2 99 99 99  3 99  4  5 99  1
294  2 99 99 99 99  4 99  3 99  1
295  2  3  4  8  7 10  5  6  9  1
296  2 99 99 99 99  3 99  4 99  1
297  2 99 99 99 99  3  4 99 99  1
298  2 99  3  4 99  5 99 99 99  1
299  2 99 99 99  3 99 99 99  4  1
300  2  5  4  3  6 99 99 99 99  1
301  2 99 99 99 99 99  4 99  3  1
302  2 10  3  4  6  9  5  7  8  1
303  2 99  5 99 99  3 99 99  4  1
304  2  3  6  7  8  4  9  5 10  1
305  2  5 99 99 99 99 99  4  3  1
306  2  3 99 99 99 99 99  4 99  1
307  2  3 10  8  7  4  9  5  6  1
308  2 99 99 99 99  3 99  2  3  1
309  2  3 99 99 99 99  4 99 99  1
310  2  9  4  5  6  7  3 10  8  1
311  2  3  6  4 99 99 99 99  5  1
312  2 99 99  4 99 99 99 99  3  1
313  2 10  3  9  6  5  8  7  4  1
314  2 99 99 99 99  3 99  4 99  1
315  2  3  5  8  7  6  9  4 10  1
316  2 99 99  3 99 99  4 99 99  1
317  2  3  7  6  8  4  9  5 10  1
318  2  4 99  3 99 99  5 99 99  1
319  2 99  5  3  4 99  6 99 99  1
320  2  3  6 10  5  4  7  8  9  1
321  2  4  7  8  5  9 10  3  6  1
322  2 99 99  5  3 99  4 99 99  1
323 99 99  4 99  1 99 99 99  3  2
324 99 99 99 99  1 99 99  3  4  2
325 99 99 99 99  1 99 99 99 99 99
326 99 99 99 99  1 99 99 99 99  2
327  2 99  3 99  1 99 99 99 99 99
328  4 99  5  3 99 99  1 99 99  2
329  5 99  2  4 99  3  1 99 99 99
330 99 99 99  2 99 99  1 99 99  3
331 99 99 99  2 99 99  1  4 99  3
332 99 99  3  2  4  5  1 99 99 99
333  3  5 99 99 99  4  1  6 99  2
334  5 99  6  4  2 99  1 99  3 99
335  2  3 99 99 99 99  1 99 99 99
336 99  3  2 99 99 99  1 99 99 99
337  6  3  7  2  4 10  1  8  9  5
338 99  4  5 99 99  2  1 99  3 99
339 99  3 99  4 99 99  1  2 99 99
340 99 99 99 99 99 99  1 99 99 99
341  8  9  7  2  3  4  1 10  5  6
342  2  3  5  6  9 10  1  4  8  7
343  2  7  3  4  9  8  1 10  6  5
344  5  4  9  3  8 10  1  7  2  6
345 99 99 99 99 99 99  1 99 99 99
346  2 99 99  4  3 99  1  6  7  5
347  4  9  7 10  3  2  1  8  6  5
348  9  8  7  2 10  6  1  5  4  3
349  3 99 99 99 99 99  2 99 99  1
350 99  4 99 99 99 99  2 99  3  1
351 99 99 99 99 99 99  2  3  4  1
352 99 99 99 99 99 99  2 99 99  1
353  3 99 99 99  4 99  2 99 99  1
354  3  4  8  7 10  9  2  6  5  1
355  3 99 99 99 99 99  2 99  4  1
356 99  4 99  3 99 99  2 99 99  1
357  5  8  7  3 10  4  2  9  6  1
358 99 99 99  3  4 99  2 99 99  1
359 99  4 99  3 99 99  2 99 99  1
360 99  4 99 99 99  3  2 99 99  1
361  4  3 99 99 99 99  2 99 99  1
362 99  3 99  4 99 99  2 99 99  1
363 99 99 99 99 99 99  3 99  2  1
364 99 99 99 99  4 99  2  3  1 99
365  3  7  8 10  9  6  4  2  5  1
366  5  9 10  6  8  4  3  2  7  1
367  7  4  2  6  8  5  3 10  9  1
368 99  4 99 99  3  1  2 99 99 99
369  3  7  6 10  9  1  2  4  8  5
370  3  4 99 99 99  1  2 99 99  5
371  4  2 99 99 99  1 99  3 99 99
372  5  6  7 10  8  1  2  3  9  4
373  4  3  5  9  8  1  6 10  7  2
374  4  8  5  9  7  1  3 99  2  6
375  2  4  3  5  6  1 10  8  9  7
376  5  9  2 10  3  1  6  7  4  8
377 99  2 99 99 99  1  3 99  4  5
378  6  7 10  9  5  1  2  9  4  3
379  3  2 99  4 99  1 99 99 99 99
380  5  6  4 10  3  1  2  7  9  8
381  5  4  7  8  1  3  6  9 10  2
382  2  5 99 99  1  4 99 99  3 99
383  3  6  7  9  1  2  8  5  4 10
384 99  2  5 99  3  1  4 99 99 99
385  4 99  3 99 99  1 99 99 99  2
386  4 99 99 99  2  1 99 99 99  3
387 99 99  3 99 99  1  2 99 99 99
388 99 99  3 99 99  1  4 99 99  2
389 99 99 99 99 99  1  3  4 99  2
390 99 99  5 99 99  1 99  3  4  2
391  5 99  3 99 99  1  4 99  6  2
392 99 99 99 99  2  1  5 99  3  4
393  4 99  5 99 99  2 99 99  1  3
394 99 99 99 99  1  2  3 99  4 99
395 99 99  1 99  2  3 99  4 99 99
396 99 99  2 99  1  3 99  4 99  5
397 99 99  4 99  3  1  2 99 99 99
398  3 99 99 99 99  1 99 99 99  2
399 99 99 99 99 99  1 99 99 99  2
400 99 99  2 99 99  1 99 99 99 99
401  1  7  5  2 10  8  6  9  3  4
402  1 99  3 99 99 99  2  4 99 99
403  1  6  8  2  9  5  7  4 10  3
404  1 99 99  2 99 99 99 99 99  3
405  1 99 99 99 99 99  2 99 99  3
406  1  4 99 99 99 99 99  2 99  3
407  1 99 99  5  4 99 99 99  3  2
408  1 99  4  5 99  6  3  7  8  2
409  1 99  5  3  4 99  2 99 99 99
410  1 10  9  8  6  4  7  2  5  3
411  1 99  3  2 99 99  4 99 99 99
412  1  3 99 99  2  4 99 99 99 99
413  1 10  6  4  9  8  3  7  2  5
414  1 99 99 99 99  2 99 99 99 99
415  1 99  2 99 99 99 99  3 99  4
416  1  4 99 99 99  3  2 99 99  5
417  1  3 99 99 99  2 99 99  4 99
418  1 99 99  4 99  5  3 99 99  2
419  1  7  4  7  8  9  3  5  6  2
420  1 99 99 99 99  2  3 99 99  4
421  1  6  3  7  2  9  5  4 10  8
422  1 99  2  7  8  9  3  4  6  5
423  1 99 99  2 99 99  3 99 99 99
424  1 10  9  2  5  3  7  6  8  4
425  1  3 99 99 99 99 99  4 99  2
426  1 99 99 99 99  2 99 99 99  3
427  1  6 99 99  3 99 99  4  5  2
428  1  8  9  4  7  2  3 10  6  5
429  1  6 10  3  9  7  8  2  4  5
430  1 99 99 99 99  4  3 99 99  2
431  1  9  2  8  3 10  4  6  7  5
432  1  4 99 99 99 99 99  3 99  2
433  1 99  3 99 99 99  4 99 99  2
434  1 99 99 99 99 99 99 99 99  2
435  1 99  3 99 99  2 99 99  5  4
436  1 99  2  3  5 99  4 99 99  6
437  1 99 99 99 99  2  3 99 99  4
438  1  4 10  6  5  8  2  9  3  7
439  1 99 99  3 99 99  4 99 99  2
440  1 99 99 99 99 99  2  4  3 99
441  1  6  2  5  3  9 10  7  4  8
442  1  8  9  2  4  7 10  5  6  3
443  1 99 99 99 99 99  2 99 99 99
444  1  2 99 99 99 99  4 99  5  3
445  1  7  8  9  6  4 10  3  5  2
446  1  3 99 99 99  5 99  4 99  2
447  1 99  2  4  3 99 99 99 99 99
448 99  1 99 99 99 99 99 99 99 99
449  1  4 99  5 99  3 99 99 99  2
450  1  2  6  9  5  7  8  3 10  4
451  1  2  3 99 99 99  4 99 99 99
452  1  3 99  4 99 99 99 99 99  2
453  1 99 99  2  3 99 99 99 99  4
454  1  3  2  8  7 10  9  6  4  5
455  1 99 99  3 99  4 99 99 99  2
456  1 99 99 99 99  2 99  4 99  3
457  1  6 10  2  5  8  3  9  4  7
458  1  4 10  5  9  8  6  2  7  3
459  1 99  3  2 99 99 99 99 99 99
460  1  3  7  2 10  8  6  9  4  5
'''

        # From A53_prop.dat (A C D I against H)
        expected = '''\
115.905886 1 1 1 1
53.964692 1 1 1 3
22.199966 1 1 3 1
27.040269 1 1 3 3
29.879240 1 3 1 1
33.326877 1 3 1 3
16.617881 1 3 3 1
50.416539 1 3 3 3
3.836185 3 1 1 1
5.205177 3 1 1 3
5.847293 3 1 3 1
6.748195 3 1 3 3
7.139208 3 3 1 1
15.275312 3 3 1 3
8.449341 3 3 3 1
58.147937 3 3 3 3
'''

        candidates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        helper = SchulzeHelper()
        helper.required_winners = 4
        helper.standardize_ballots([
            {"count": 1, "ballot": dict(zip(candidates, [int(r) for r in line.split()[1:]]))}
            for line in A53.splitlines()
        ], helper.BALLOT_NOTATION_RANKING)
        helper.generate_completed_patterns()
        completed = helper.proportional_completion('h', ('a', 'c', 'd', 'i'))
        self.assertEqual(
            sorted((pattern, round(weight, 6))
                   for (pattern, weight) in completed.items()),
            [(tuple(int(r) for r in line.split()[1:]), float(line.split()[0]))
             for line in expected.splitlines()])

if __name__ == "__main__":
    unittest.main()
