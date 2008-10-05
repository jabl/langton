Langton's ant
=============

This is an enhanced version of the Langton's ant cellular automata.  It
supports multiple ants, each with random programs.

The original Langton's ant
--------------------------

This is a cellular automata where you have an 'ant' that moves around on a
grid. The grid squares are either black or white. If the ant hits a black
square it changes the color to white and turns to the right; if the ant hits a
white square it changes it to black and turns to the left.

The 'enhanced' version in this program
--------------------------------------

This program supports a configurable number of ants and possible colors. Each
ant has a randomized program. The program tells for each color, which color to
change the grid square to, and to turn in which direction (left, right,
forward, back).

Installation
------------

You can run the program from the directory where you unpacked it, or you can
run the python distutils installer via ``python setup.py install
--prefix=$HOME`` to install it to your home directory.

The program depends on `NumPy <http://numpy.scipy.org>`_ and `wxPython
<http://wxpython.org>`_ .

Running the program
-------------------

Just run ``./langton.py``.
