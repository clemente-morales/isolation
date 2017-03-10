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
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - (2 * opp_moves))


class CustomPlayer:
    """Game-playing agent that chooses a move using the evaluation function (custom_score)
    and a depth-limited minimax algorithm with alpha-beta pruning.
    
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
        
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
        
    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).
        
    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().
        
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        This function perform iterative deepening if self.iterative=True,
        and it uses the search method (minimax or alphabeta) corresponding
        to the self.method value.
        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
            
        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.
            
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        
        selected_move = (-1, -1)
        depth = self.search_depth
        depth+=1
        
        if not legal_moves:
            return selected_move
        
        if game.move_count == 0:
            selected_move = self.get_open_game_move(game)
            return selected_move

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
        """ Allows to get the best move using minimax or alphabeta algorithm based on 
        the method selection.
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
            
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        Returns
        -------
        float
            The score for the current search branch
            
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.method == 'minimax':
            (utility, move) = self.minimax(game, depth)
            return move
        elif self.method == 'alphabeta':
            (utility, move) = self.alphabeta(game, depth)
            return move
                    

    def minimax(self, game, depth):
        """ minimax search algorithm.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
            
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        Returns
        -------
        float
            The score for the current search branch
            
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
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
    

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Minimax search with alpha-beta pruning.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
            
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
            
        beta : float
            Beta limits the upper bound of search on maximizing layers
            
        Returns
        -------
        float
            The score for the current search branch
            
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
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
    
    def get_open_game_move(self, game):
        row = game.height//2
        col = game.width//2
        return (row, col)
        
    
        
    
    

