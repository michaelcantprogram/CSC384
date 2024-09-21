############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 1 Starter Code
## v1.0
############################################################

from typing import List
import heapq
from heapq import heappush, heappop
import time
import argparse
import math # for infinity

from board import *

def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """
    curr_board = state.board
    if len(curr_board.boxes) != len(set(curr_board.boxes)):
        return False
    for box in curr_board.boxes:
        if box not in curr_board.storage:
            return False
    return True


def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    _path = []
    curr_state = state
    while curr_state:
        _path.append(curr_state)
        curr_state = state.parent
    return _path[::-1]


def is_space(curr_board: Board, coor: tuple) -> bool:
    """
    Check if the given coordinate is not a space.

    :param curr_board: The current board.
    :type curr_board: Board
    :param coor: The coordinate to check.
    :type coor: tuple
    :return: True if the coordinate is not a space, False otherwise.
    :rtype: bool
    """
    if coor in curr_board.boxes or coor in curr_board.obstacles or coor in curr_board.robots:
        return False
    return True


def copy_board(board: Board) -> Board:
    """
    Return a deep copy of the given board.

    :param board: The board to copy.
    :type board: Board
    :return: The copied board.
    :rtype: Board
    """
    return Board(board.name, board.width, board.height, board.robots[:],
                 board.boxes[:], board.storage[:], board.obstacles[:])


def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """
    successors = []
    curr_board = state.board
    for robot_coor in curr_board.robots:
        right_move = (robot_coor[0] + 1, robot_coor[1])
        left_move = (robot_coor[0] - 1, robot_coor[1])
        up_move = (robot_coor[0], robot_coor[1] - 1)
        down_move = (robot_coor[0], robot_coor[1] + 1)
        for move in [right_move, left_move, up_move, down_move]:
            if is_space(curr_board, move):
                new_board = copy_board(curr_board)
                if new_board == curr_board:
                    print("new board initialization failed")
                new_board.robots.remove(robot_coor)
                new_board.robots.append(move)
                new_state = State(new_board, state.hfn, state.f, state.depth + 1, state)
                successors.append(new_state)
            elif move in curr_board.boxes:
                box_next_move = (move[0] + (move[0] - robot_coor[0]), move[1] + (move[1] - robot_coor[1]))
                if is_space(curr_board, box_next_move):
                    new_board = copy_board(curr_board)
                    new_board.robots.remove(robot_coor)
                    new_board.robots.append(move)
                    new_board.boxes.remove(move)
                    new_board.boxes.append(box_next_move)
                    new_state = State(new_board, state.hfn, state.f, state.depth + 1, state)
                    successors.append(new_state)
    return successors


def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """

    raise NotImplementedError


def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic (a function that consumes a Board and produces a numeric heuristic value)
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """

    raise NotImplementedError


def heuristic_basic(board):
    """
    Returns the heuristic value for the given board
    based on the Manhattan Distance Heuristic function.

    Returns the sum of the Manhattan distances between each box 
    and its closest storage point.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    raise NotImplementedError


def heuristic_advanced(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    raise NotImplementedError


def solve_puzzle(board: Board, algorithm: str, hfn):
    """
    Solve the given puzzle using the given type of algorithm.

    :param algorithm: the search algorithm
    :type algorithm: str
    :param hfn: The heuristic function
    :type hfn: Optional[Heuristic]

    :return: the path from the initial state to the goal state
    :rtype: List[State]
    """

    print("Initial board")
    board.display()

    time_start = time.time()

    if algorithm == 'a_star':
        print("Executing A* search")
        path, step = a_star(board, hfn)
    elif algorithm == 'dfs':
        print("Executing DFS")
        path, step = dfs(board)
    else:
        raise NotImplementedError

    time_end = time.time()
    time_elapsed = time_end - time_start

    if not path:

        print('No solution for this puzzle')
        return []

    else:

        print('Goal state found: ')
        path[-1].board.display()

        print('Solution is: ')

        counter = 0
        while counter < len(path):
            print(counter + 1)
            path[counter].board.display()
            print()
            counter += 1

        print('Solution cost: {}'.format(step))
        print('Time taken: {:.2f}s'.format(time_elapsed))

        return path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The file that contains the solution to the puzzle."
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        choices=['a_star', 'dfs'],
        help="The searching algorithm."
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        required=False,
        default=None,
        choices=['zero', 'basic', 'advanced'],
        help="The heuristic used for any heuristic search."
    )
    args = parser.parse_args()

    # set the heuristic function
    heuristic = heuristic_zero
    if args.heuristic == 'basic':
        heuristic = heuristic_basic
    elif args.heuristic == 'advanced':
        heuristic = heuristic_advanced

    # read the boards from the file
    board = read_from_file(args.inputfile)

    # solve the puzzles
    path = solve_puzzle(board, args.algorithm, heuristic)

    # save solution in output file
    outputfile = open(args.outputfile, "w")
    counter = 1
    for state in path:
        print(counter, file=outputfile)
        print(state.board, file=outputfile)
        counter += 1
    outputfile.close()