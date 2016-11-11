Python Vote Core
================

python-vote-core implements various electoral methods, providing the results
calculated off a provided set of ballots and options.

* Project page: http://github.com/bradbeattie/python-vote-core
* Issue tracker: http://github.com/bradbeattie/python-vote-core/issues
* Example usage: http://modernballots.com

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

    >>> from pyvotecore.schulze_method import SchulzeMethod
    >>> from pyvotecore.condorcet import CondorcetHelper
    >>> ballots = [
    ...   { "count":3, "ballot":[["A"], ["C"], ["D"], ["B"]] },
    ...   { "count":9, "ballot":[["B"], ["A"], ["C"], ["D"]] },
    ...   { "count":8, "ballot":[["C"], ["D"], ["A"], ["B"]] },
    ...   { "count":5, "ballot":[["D"], ["A"], ["B"], ["C"]] },
    ...   { "count":5, "ballot":[["D"], ["B"], ["C"], ["A"]] }
    ... ]
    >>> SchulzeMethod(ballots, ballot_notation = CondorcetHelper.BALLOT_NOTATION_GROUPING).as_dict()
    {'actions': [{'edges': {('A', 'B')}},
      {'edges': {('A', 'C')}},
      {'nodes': {'A'}},
      {'edges': {('B', 'C')}},
      {'nodes': {'B', 'D'}}],
     'candidates': {'A', 'B', 'C', 'D'},
     'pairs': {('A', 'B'): 16,
      ('A', 'C'): 17,
      ('A', 'D'): 12,
      ('B', 'A'): 14,
      ('B', 'C'): 19,
      ('B', 'D'): 9,
      ('C', 'A'): 13,
      ('C', 'B'): 11,
      ('C', 'D'): 20,
      ('D', 'A'): 18,
      ('D', 'B'): 21,
      ('D', 'C'): 10},
     'strong_pairs': {('A', 'B'): 16,
      ('A', 'C'): 17,
      ('B', 'C'): 19,
      ('C', 'D'): 20,
      ('D', 'A'): 18,
      ('D', 'B'): 21},
     'winner': 'C'}
