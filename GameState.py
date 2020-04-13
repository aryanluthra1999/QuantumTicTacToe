from Board import QBoard
from Player import Player

class GameState:

    def __init__(self):
        self.board = QBoard()
        self.playerx = Player('x')
        self.playero = Player('o')
        self.curr_turn = 'x'
        

    @staticmethod
    def assign_players():
        #TODO: make a random assigner of players
        return p1, p2

