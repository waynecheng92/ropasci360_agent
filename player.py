from neverland.util import *
import random

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        self.state = {"upper": [], "lower": [], "upThrow": 0, "lowThrow": 0, "action": []}
        self.color = player

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here
        depth = best_depth(self.state)
        if direct_eat(self.state,self.color):
            return direct_eat(self.state,self.color)
        elif in_danger(self.state,self.color):
            return in_danger(self.state,self.color)
        elif direct_throw(self.state,self.color):
            return direct_throw(self.state,self.color)
        elif chase(self.state,self.color):
            return chase(self.state,self.color)
        else:
            return ab_minimax(self.state, self.color, depth, -9999, 9999, True, self.color)[1]["action"][0]
        

    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        self.state = do_actions(self.state, self.color, opponent_action, player_action)
        self.state = remove_beaten(self.state)
        

