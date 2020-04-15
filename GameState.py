from Board import QBoard
from Player import Player

class GameState:

    def __init__(self):
        self.board = QBoard()
        self.playerx = Player('x') # 'x'
        self.playero = Player('o') # 'o'



    @staticmethod
    def assign_players():
        #TODO: make a random assigner of players
        return p1, p2

    def next_turn(self):
        if QBoard.cycle:
            ### Prompt Collapse from board
        else:
            ### Prompt regular turn
    

