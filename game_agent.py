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
        
        selected_move = (-1, -1)
        depth = self.search_depth
        depth+=1

        try:
            if self.iterative == True:
                while True:
                    depth+=1
                    temp = self.get_best_move(game, depth)
                    if temp is not None:
                        selected_move = temp
                        
                    if self.time_left() < self.TIMER_THRESHOLD:
                        raise Timeout()
            else:
                selected_move = self.get_best_move(game, self.search_depth)
                
        except Timeout:
            pass

        return selected_move
    
    def get_best_move(self, game, depth) :
        if self.method == 'minimax':
            (utility, move) = self.minimax(game, depth, True)
            return move
        elif self.method == 'alphabeta':
            (utility, move) = self.alphabeta(game, depth)
            return move
                    

    def minimax(self, game, depth, maximizing_player=True):
        utilities = [] 

        try:
            for move in game.get_legal_moves():
                new_game = game.forecast_move(move)
                utility = self.min_value(new_game, depth-1)
                utilities.append((utility, move))
        except Timeout:
            pass
        
        if not utilities:
            return (0, None)
        
        (utility, selected_move) = max(utilities, key = lambda x: x[0])
        return (utility, selected_move) 
    
    def max_value(self, game, depth) :
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        if depth <= 0:
            return self.score(game, game.active_player)            
        
        utility = float("-inf")
         
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            utility = max(utility, self.min_value(new_game, depth-1))
                        
        return utility
    
    def min_value(self, game, depth) :
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        if depth <= 0:
            return self.score(game, game.inactive_player)                    
        
        utility = float("inf")
        
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            utility = min(utility, self.max_value(new_game, depth-1))
        return utility
    

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        def alphabeta_max_value(game, depth, alpha, beta):
            if depth == 0:
                return self.score(game, game.active_player)
            
            utility = float("-inf")
            
            for move in game.get_legal_moves():
                new_game = game.forecast_move(move)
                utility = max(utility, alphabeta_min_value(new_game, depth-1, alpha, beta))
                if utility >= beta:
                    return utility
                alpha = max(alpha, utility)
            return utility
    
        def alphabeta_min_value(game, depth, alpha, beta):
            if depth == 0:
                return self.score(game, game.inactive_player)
            
            utility = float("inf")
            
            for move in game.get_legal_moves():
                new_game =  game.forecast_move(move)
                utility = min(utility, alphabeta_max_value(new_game, depth-1, alpha, beta))
                if utility <= alpha:
                    return utility
                beta = min(beta, utility)
                
            return utility
        
        utility = alphabeta_max_value(game, depth, alpha, beta) 

        selected_move = None
        
         
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            
            if hasattr(game, 'counter'):
                game.counter[move] -= 1
                 
            game_utility = self.score(new_game, new_game.active_player)
            if utility == game_utility:
                selected_move = move
                break
                   
        return (utility, selected_move)
        
    
    

