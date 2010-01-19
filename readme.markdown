# Election Web Service

Election Web Service exposes implmentations of various election methods through
a JSON interface. The purpose of this is to eliminate the need to implement
language-specific versions of these methods wherever an internet connection is
available.

* Project page: <http://github.com/bradbeattie/Election-Web-Service>
* Issue tracker: <http://github.com/bradbeattie/Election-Web-Service/issues>
* Active server: <http://vote.cognitivesandbox.com>
* Example usage: <http://modernballots.com>

## Methods implemented

* Plurality (aka first-past-the-post or fptp)
* Plurality at large (aka block voting)
* Instant-Runoff Voting (aka IRV)
* Single Transferable Vote (aka STV)
* Ranked Pairs (aka Tideman)
* Schulze Method (aka Beatpath)
* Schulze STV

## Installation
  
    python webserver.py
  
## Basic Usage

    curl -d '{"voting_system": "stv", "ballots": [{"count": 4, "ballot": ["orange"]}, {"count": 2, "ballot": ["pear", "orange"]}, {"count": 8, "ballot": ["chocolate", "strawberry"]}, {"count": 4, "ballot": ["chocolate", "sweets"]}, {"count": 1, "ballot": ["strawberry"]}, {"count": 1, "ballot": ["sweets"]}], "winners": 3}' http://vote.cognitivesandbox.com;
    
    curl -d '{"voting_system": "schulze_method", "notation": "ranking", "ballots": [{ "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2 }}, { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9 }}, { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9 }}]}' http://vote.cognitivesandbox.com;
    
    curl -d '{"voting_system": "schulze_stv", "notation": "ranking", "ballots": [{ "count":1, "ballot":{"A":9, "B":1, "C":1, "D":9, "E":9, "F":2 }}, { "count":1, "ballot":{"A":3, "B":2, "C":3, "D":1, "E":9, "F":9 }}, { "count":1, "ballot":{"A":9, "B":9, "C":9, "D":9, "E":1, "F":9 }}], "winners": 2}' http://vote.cognitivesandbox.com;

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