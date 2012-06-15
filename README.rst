======
Conway
======

Conway is a dead-simple implementation of Conway's Game Of Life using my
`Blessings terminal library`_. It detects your terminal size and color depth
and blits a lovely cellular automaton for your ogling pleasure.

.. _Blessings terminal library: http://pypi.python.org/pypi/blessings/


Features
========

* Simple implementation
* Pretty colors
* Few calories
* Nudges itself out of repetitive patterns

Rather than having a zillion features, Conway focuses on clarity of
implementation. It's fun to hack on. Try implementing different ``wrap``
parameters for ``next_board``!


Getting it running
==================

::

    pip install conway
    conway.py

You should see life explode before your eyes. When you're done, hit control-C,
and it'll clean up nicely after itself.


Kudos
=====

Ripped off a really elegant implementation of the algorithm from Jack Diedrich
(and ruined it).


Version History
===============

1.1
  * Use "fullscreen mode" so we don't leave a big white screen behind
    afterward.

1.0
  * Initial release