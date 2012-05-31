#!/usr/bin/env python
from itertools import chain
from random import randint
from sys import stdout
from time import sleep

from blessings import Terminal


def main():
    """Play Conway's Game of Life on the terminal."""
    def die((x, y)):
        if not (x < 0 or x >= term.width or
                y < 0 or y >= term.height):
            return x, y

    term = Terminal()
    board = random_board(term.width - 1, term.height - 1)

    print term.civis,  # hide cursor
    print term.clear,
    while True:
        try:
            board = next_board(board, wrap=die)
            draw(board, term)
            sleep(0.05)
        except KeyboardInterrupt:
            print term.cnorm,
            stdout.flush()
            break
        finally:
            clear(board, term)


def random_board(max_x, max_y):
    """Return a random board with given max x and y coords."""
    LOAD_FACTOR = 10  # Smaller means more crowded.
    board = {}
    for _ in range(int(max_x * max_y / LOAD_FACTOR)):
        board[(randint(0, max_x), randint(0, max_y))] = 0
    return board


def clear(board, term):
    """Clear the droppings of the given board, without flushing."""
    for x, y in board.iterkeys():
        print term.move(y, x) + ' ',


def draw(board, term, colors=(9, 10, 14)):
    """Draw a set of points to the terminal, and flush."""
    for (x, y), state in board.iteritems():
        print term.move(y, x) + term.on_color(colors[state])(' '),
    stdout.flush()


def next_board(board, wrap=lambda p: p):
    """Given a set of "on" (x, y) points, return the next set.

    Adapted from Jack Diedrich's implementation from his 2012 PyCon talk "Stop
    Writing Classes"

    :arg wrap: A callable which takes a point and transforms it, for example
        to wrap to the other edge of the screen. Return None to remove a point.

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
    """Return the (possibly out of bounds) neighbors of a point."""
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
