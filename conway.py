#!/usr/bin/env python
"""Conway's Game of Life, drawn to the terminal care of the Blessings lib

A board is represented like this::

    {(x, y): state,
     ...}

...where ``state`` is an int from 0..2 representing a color.

"""
from itertools import chain
from random import randint
from sys import stdout
from time import sleep

from blessings import Terminal


def main():
    """Play Conway's Game of Life on the terminal."""
    def die((x, y)):
        """Pretend any out-of-bounds cell is dead."""
        if 0 <= x < width and 0 <= y < height:
            return x, y

    term = Terminal()
    width = term.width
    height = term.height
    board = random_board(width - 1, height - 1)
    cells = cell_strings(term)

    print term.civis,  # hide cursor
    print term.clear,
    while True:
        try:
            board = next_board(board, die)
            draw(board, term, cells)
            stdout.flush()
            sleep(0.05)
        except KeyboardInterrupt:
            break
        finally:
            clear(board, term, height)
    print term.cnorm


def cell_strings(term):
    """Return the strings that represent each possible living cell state.

    Return the most colorful ones the terminal supports.

    """
    num_colors = term.number_of_colors
    if num_colors >= 16:
        funcs = term.on_bright_red, term.on_bright_green, term.on_bright_cyan
    elif num_colors >= 8:
        funcs = term.on_red, term.on_green, term.on_blue
    else:
        # For black and white, use the checkerboard cursor from the vt100
        # alternate charset:
        return (term.reverse(' '),
                term.smacs + term.reverse('a') + term.rmacs,
                term.smacs + 'a' + term.rmacs)
    # Wrap spaces in whatever pretty colors we chose:
    return [f(' ') for f in funcs]


def random_board(max_x, max_y):
    """Return a random board with given max x and y coords."""
    LOAD_FACTOR = 9  # Smaller means more crowded.
    return dict(((randint(0, max_x), randint(0, max_y)), 0) for _ in
                xrange(int(max_x * max_y / LOAD_FACTOR)))


def clear(board, term, height):
    """Clear the droppings of the given board."""
    for y in xrange(height):
        print term.move(y, 0) + term.clear_eol,


def draw(board, term, cells):
    """Draw a board to the terminal."""
    for (x, y), state in board.iteritems():
        with term.location(x, y):
            print cells[state],


def next_board(board, wrap):
    """Given a board, return the board one interation later.

    Adapted from Jack Diedrich's implementation from his 2012 PyCon talk "Stop
    Writing Classes"

    :arg wrap: A callable which takes a point and transforms it, for example
        to wrap to the other edge of the screen. Return None to remove a point.

    """
    new_board = {}

    # We need consider only the points that are alive and their neighbors:
    points_to_recalc = set(board.iterkeys()) | set(chain(*map(neighbors, board)))

    for point in points_to_recalc:
        count = sum((neigh in board) for neigh in
                    (wrap(n) for n in neighbors(point) if n))
        if count == 3:
            state = 0 if point in board else 1
        elif count == 2 and point in board:
            state = 2
        else:
            state = None

        if state is not None:
            wrapped = wrap(point)
            if wrapped:
                new_board[wrapped] = state

    return new_board


def neighbors((x, y)):
    """Return the (possibly out of bounds) neighbors of a point."""
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y - 1
    yield x - 1, y + 1
    yield x - 1, y - 1


if __name__ == '__main__':
    main()
