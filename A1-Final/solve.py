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
    return set(state.board.boxes) == set(state.board.storage)


def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    state_path = []
    curr_state = state
    while curr_state:
        state_path.append(curr_state)
        curr_state = curr_state.parent
    state_path.reverse()
    return state_path


def is_space(curr_board: Board, coor: tuple) -> bool:
    """
    Helper, check if the given coordinate is not a space.

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


def init_new_board(board: Board, robot_remove: tuple, robot_add: tuple,
                   box_remove=None, box_add=None) -> Board:
    """
    Helper, return a new board with the given changes.

    :param board: the current board
    :param robot_remove: the robot to remove
    :param robot_add: the robot to add
    :param box_remove: the box to remove, if any
    :param box_add: the box to add, if any
    :return: a new board with the given changes
    """
    new_board = Board(board.name, board.width, board.height, board.robots[:],
                 board.boxes[:], board.storage, board.obstacles)
    new_board.robots.remove(robot_remove)
    new_board.robots.append(robot_add)
    if box_remove:
        new_board.boxes.remove(box_remove)
    if box_add:
        new_board.boxes.append(box_add)
    return new_board


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
                new_board = init_new_board(curr_board, robot_coor, move)
                new_state = State(new_board,
                                  state.hfn,
                                  state.depth + 1 + state.hfn(new_board),
                                  state.depth + 1, state)
                successors.append(new_state)
            elif move in curr_board.boxes:
                box_next_move = (move[0] + (move[0] - robot_coor[0]),
                                 move[1] + (move[1] - robot_coor[1]))
                if is_space(curr_board, box_next_move):
                    new_board = init_new_board(curr_board,
                                               robot_coor,
                                               move, move,
                                               box_next_move)
                    new_state = State(new_board, state.hfn,
                                      state.f, state.depth + 1, state)
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
    init_state = State(init_board, heuristic_zero, 0, 0)
    frontier = [init_state]
    explored = set()
    while frontier:
        curr_state = frontier.pop()
        # state_board = curr_state.board
        # board_hash = hash(state_board)
        board_hash = curr_state.id
        if board_hash in explored:
            continue
        explored.add(board_hash)
        if is_goal(curr_state):
            return get_path(curr_state), curr_state.depth
        successors = get_successors(curr_state)
        frontier.extend(successors)
    return [], -1



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
    init_state = State(init_board, hfn, hfn(init_board), 0)
    frontier = []
    heapq.heappush(frontier, (init_state.f, init_state))
    explored = set()

    while frontier:
        _, curr_state = heapq.heappop(frontier)
        # state_board = curr_state.board
        # board_hash = hash(state_board)
        board_hash = curr_state.id
        if board_hash not in explored:
            explored.add(board_hash)
            if is_goal(curr_state):
                return get_path(curr_state), curr_state.depth
            successors = get_successors(curr_state)
            for succ in successors:
                succ.f = succ.depth + succ.hfn(succ.board)
                heapq.heappush(frontier, (succ.f, succ))
    return [], -1


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
    total_distance = 0
    for box in board.boxes:
        min_distance = board.height + board.width
        for storage in board.storage:
            distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance
    return total_distance


def check_deadlock(box: list, walls: list) -> bool:
    """
    Helper, check if the given box is in a deadlock state.

    :param box: The box to check.
    :type box: list
    :param walls: The walls on the board.
    :type walls: list
    :return: True if the box is in a deadlock state, False otherwise.
    """
    box_up = (box[0], box[1] - 1)
    box_down = (box[0], box[1] + 1)
    box_left = (box[0] - 1, box[1])
    box_right = (box[0] + 1, box[1])
    if box_up in walls or box_down in walls:
        if box_left in walls or box_right in walls:
            return True
    if box_left in walls or box_right in walls:
        if box_up in walls or box_down in walls:
            return True
    return False


def heuristic_advanced(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    boxes = board.boxes
    walls = board.obstacles
    storages = board.storage
    for box in boxes:
        if box in storages:
            continue
        if check_deadlock(box, walls):
            return math.inf
    return heuristic_basic(board)


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