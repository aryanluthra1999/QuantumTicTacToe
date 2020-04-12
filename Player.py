class Player:
    def __init__(self, team):
        assert team == 'x' or team == 'o'
        self.team = team
