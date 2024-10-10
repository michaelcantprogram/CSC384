###############################################################################
# This file implements various alpha-beta pruning agents.
#
# CSC 384 Assignment 2 Starter Code
# version 2.0
###############################################################################
from wrapt_timeout_decorator import timeout

from mancala_game import play_move
from utils_old import *


def alphabeta_max_basic(board, curr_player, alpha, beta, heuristic_func):
    """
    Perform Alpha-Beta Search for MAX player.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :return the best move and its minimax value.
    """
    possible_moves = board.get_possible_moves(curr_player)
    opponent = get_opponent(curr_player)
    if not possible_moves:
        return None, heuristic_func(board, curr_player)
    best_move = None
    best_value = float('-inf')
    for move in possible_moves:
        new_board = play_move(board, curr_player, move)
        _, value = alphabeta_min_basic(new_board, opponent, alpha, beta, heuristic_func)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)
        if alpha >= beta:
            break
    return best_move, best_value


def alphabeta_min_basic(board, curr_player, alpha, beta, heuristic_func):
    """
    Perform Alpha-Beta Search for MIN player.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :return the best move and its minimax value.
    """
    possible_moves = board.get_possible_moves(curr_player)
    opponent = get_opponent(curr_player)
    if not possible_moves:
        return None, heuristic_func(board, opponent)
    best_move = None
    best_value = float('inf')
    for move in possible_moves:
        new_board = play_move(board, curr_player, move)
        _, value = alphabeta_max_basic(new_board, opponent, alpha, beta, heuristic_func)
        if value < best_value:
            best_value = value
            best_move = move
        beta = min(beta, best_value)
        if alpha >= beta:
            break
    return best_move, best_value


def alphabeta_max_limit(board, curr_player, alpha, beta, heuristic_func, depth_limit):
    """
    Perform Alpha-Beta Search for MAX player up to the given depth limit.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :return the best move and its estimated minimax value.
    """

    raise NotImplementedError

def alphabeta_min_limit(board, curr_player, alpha, beta, heuristic_func, depth_limit):
    """
    Perform Alpha-Beta Search for MIN player up to the given depth limit.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :return the best move and its estimated minimax value.
    """

    raise NotImplementedError

def alphabeta_max_limit_opt(board, curr_player, alpha, beta, heuristic_func, depth_limit, optimizations):
    """
    Perform Alpha-Beta Search for MAX player 
    up to the given depth limit and with additional optimizations.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its estimated minimax value.
    """

    raise NotImplementedError

def alphabeta_min_limit_opt(board, curr_player, alpha, beta, heuristic_func, depth_limit, optimizations):
    """
    Perform Alpha-Beta Pruning for MIN player 
    up to the given depth limit and with additional optimizations.
    Return the best move and the estimated minimax value.

    If the board is a terminal state,
    return None as the best move and the heuristic value of the board as the best value.

    :param board: the current board
    :param curr_player: the current player
    :param alpha: current alpha value
    :param beta: current beta value
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its estimated minimax value.
    """

    raise NotImplementedError


###############################################################################
## DO NOT MODIFY THE CODE BELOW.
###############################################################################

@timeout(TIMEOUT, timeout_exception=AiTimeoutError)
def run_alphabeta(curr_board, player, limit, optimizations, hfunc):
    if optimizations is not None:
        opt = True
    else:
        opt = False

    alpha = float("-Inf")
    beta = float("Inf")
    if opt:
        move, value = alphabeta_max_limit_opt(curr_board, player, alpha, beta, hfunc, limit, optimizations)
    elif limit >= 0:
        move, value = alphabeta_max_limit(curr_board, player, alpha, beta, hfunc, limit)
    else:
        move, value = alphabeta_max_basic(curr_board, player, alpha, beta, hfunc)
    
    return move, value

