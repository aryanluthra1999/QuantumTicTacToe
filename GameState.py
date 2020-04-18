from Board import QBoard


class GameState:

    def __init__(self):
        self.board = QBoard()
        self.playerx = 'x'
        self.playero = 'o'

    @staticmethod
    def assign_players():
        # TODO: make a random assigner of players
        return p1, p2

    def next_turn(self):
        if QBoard.cycle:
            ### Prompt Collapse from board
            pass
        else:
            ### Prompt New Turn from user and how it will be placed
            pass
    ### Prompt regular turn

    def get_succesors(self):
        # TODO: Returns the succesor of the current game state
        pass

    def get_place_succesors(self):
        # TODO: Helper method of get succesors in order to get all the succersor when the turn is a place turn
        pass

    def get_collapse_succesors(self):


