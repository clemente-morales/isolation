"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    pass


def custom_score(game, player):
    raise NotImplementedError


class CustomPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        self.time_left = time_left

        try:
            if self.method == 'minimax':
                (utility, move) = self.minimax(game, self.search_depth, True)
                return move
            elif self.method == 'alphabeta':
                (utility, move) = self.alphabeta(game, self.search_depth)
                return move
            pass

        except Timeout:
            pass

        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        
        utilities = [] 

        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            utility = self.min_value(new_game, depth-1)
            utilities.append((utility, move))
        
        (utility, selected_move) = max(utilities, key = lambda x: x[0])
        return (utility, selected_move) 
    
    def max_value(self, game, depth) :
        if depth == 0:
            return self.score(game, game.active_player)
        
        utility = float("-inf")
         
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            utility = max(utility, self.min_value(new_game, depth-1))
                        
        return utility
    
    def min_value(self, game, depth) :
        if depth == 0:
            return self.score(game, game.inactive_player)
        
        utility = float("inf")
        
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            utility = min(utility, self.max_value(new_game, depth-1))
        return utility

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        
        utilities = [] 

        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            utility = self.min_value(new_game, depth-1)
            utilities.append((utility, move))
        
        (utility, selected_move) = max(utilities, key = lambda x: x[0])
        return (utility, selected_move)
