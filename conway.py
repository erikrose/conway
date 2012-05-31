#!/usr/bin/env python
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
    board = set([(10, 10), (11, 10), (12, 10), (10, 11), (11, 12)])
    for i in range(50):
        draw(board, term)
        sleep(0.1)
        board = next_board(board, wrap=die)


def draw(board, term):
    """Draw a set of points to the terminal."""
    with term.location():  # snap back when done
        print term.clear,
        for x, y in board:
            print term.move(y, x) + '#',
            stdout.flush()


def next_board(board, wrap=lambda p: p):
    """Given a set of "on" (x, y) points, return the next set.

    Adapted from Jack Diedrich's implementation from his 2012 PyCon talk "Stop
    Writing Classes"

    :arg wrap: A callable which takes a point and transforms it, for example
        to wrap to the other edge of the screen

    """
    new_board = set()

    # We need consider only the points that are alive and their neighbors:
    points_to_recalc = board | set(chain(*map(neighbors, board)))

    for point in points_to_recalc:
        count = sum((neigh in board) for neigh in neighbors(point))
        x, y = point
        if count == 3 or (count == 2 and point in board):
            wrapped = wrap(point)
            if wrapped:
                new_board.add(wrapped)
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
