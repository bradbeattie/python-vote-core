# Python Vote Core

python-vote-core implements various electoral methods, providing the results
calculated off a provided set of ballots and options.

* Project page: <http://github.com/bradbeattie/python-vote-core>
* Issue tracker: <http://github.com/bradbeattie/python-vote-core/issues>
* Example usage: <http://vote.cognitivesandbox.com>, <http://modernballots.com>

## Methods implemented

* Single Winner Methods
	* Plurality (aka first-past-the-post or fptp)
	* Instant-Runoff Voting (aka IRV)
	* Schulze Method (aka Beatpath)
* Multiple Winner Methods
	* Plurality at large (aka block voting)
	* Single Transferable Vote (aka STV)
	* Schulze STV
* Ordering Methods
	* Schulze Proportional Representation
	* Schulze Nonproportional Representation

## Basic Usage

	print SchulzeMethod([
		{ "count":3, "ballot":[["A"], ["C"], ["D"], ["B"]] },
		{ "count":9, "ballot":[["B"], ["A"], ["C"], ["D"]] },
		{ "count":8, "ballot":[["C"], ["D"], ["A"], ["B"]] },
		{ "count":5, "ballot":[["D"], ["A"], ["B"], ["C"]] },
		{ "count":5, "ballot":[["D"], ["B"], ["C"], ["A"]] }
	], ballot_notation = "grouping").as_dict()

## License

Copyright (C) 2009, Brad Beattie

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
