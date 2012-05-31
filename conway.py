#!/usr/bin/env python
import atexit
from itertools import chain
from sys import stdout
from time import sleep

from blessings import Terminal


def main():
    """Play Conway's Game of Life on the terminal."""
    def die((x, y)):
        if (x < 0 or x >= term.width or
            y < 0 or y >= term.height):
            return None
        return x, y

    term = Terminal()
    board = dict(((x, y), 1) for x, y in [(10, 10), (11, 10), (12, 10), (10, 11), (11, 12)])

    # Hide the cursor, but show it on exit:
    atexit.register(stdout.write, term.cnorm)
    print term.civis,

    with term.location():  # snap back when done
        for i in range(50):
            draw(board, term)
            sleep(0.05)
            board, old_board = next_board(board, wrap=die), board
            clear(old_board, term)


def clear(board, term):
    for x, y in board.iterkeys():
        print term.move(y, x) + ' ',


def draw(board, term, colors=(9, 10, 14)):
    """Draw a set of points to the terminal."""
    for (x, y), state in board.iteritems():
        print term.move(y, x) + term.on_color(colors[state])(' '),
        stdout.flush()


def next_board(board, wrap=lambda p: p):
    """Given a set of "on" (x, y) points, return the next set.

    Adapted from Jack Diedrich's implementation from his 2012 PyCon talk "Stop
    Writing Classes"

    :arg wrap: A callable which takes a point and transforms it, for example
        to wrap to the other edge of the screen

    """
    new_board = {}

    # We need consider only the points that are alive and their neighbors:
    points_to_recalc = set(board.iterkeys()) | set(chain(*map(neighbors, board)))

    for point in points_to_recalc:
        count = sum((neigh in board) for neigh in neighbors(point))
        if count == 3:
            if point in board:
                state = 0
            else:
                state = 1
        elif count == 2 and point in board:
            state = 2
        else:
            state = None

        if state is not None:
            wrapped = wrap(point)
            if wrapped:
                new_board[wrapped] = state
                
    return new_board


def neighbors(point):
    x, y = point
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
