Python Vote Core
================

python-vote-core implements various electoral methods, providing the results
calculated off a provided set of ballots and options.

* Project page: http://github.com/bradbeattie/python-vote-core
* Issue tracker: http://github.com/bradbeattie/python-vote-core/issues
* Example usage: http://vote.cognitivesandbox.com, http://modernballots.com

Methods implemented
-------------------

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

Basic Usage
-----------

Schulze method example::

  print SchulzeMethod([
    { "count":3, "ballot":[["A"], ["C"], ["D"], ["B"]] },
    { "count":9, "ballot":[["B"], ["A"], ["C"], ["D"]] },
    { "count":8, "ballot":[["C"], ["D"], ["A"], ["B"]] },
    { "count":5, "ballot":[["D"], ["A"], ["B"], ["C"]] },
    { "count":5, "ballot":[["D"], ["B"], ["C"], ["A"]] }
  ], ballot_notation = "grouping").as_dict()

