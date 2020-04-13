import networkx as nx


class QBoard:
    def __init__(self):
        self.cells = [set() for i in range(9)]
        self.measured = dict()
        self.moves = 0
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(1, 10))
        self.cycle = False

    def is_win(self):
        wins = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],

                [1, 4, 7],
                [2, 5, 8],
                [3, 6, 9],

                [1, 5, 9],
                [3, 5, 7]]

        for win_comb in wins:
            if self.all_same(win_comb):
                return True
        return False

    def all_same(self, loc_list):
        contents = {self.measured[loc] if loc in self.measured else -1}
        if -1 in set:
            return False
        elif len(contents) == 1:
            return True
        else:
            return False

    def make_move(self, type, *args):
        assert type == "collapse" or type == "place"
        if type == "place":
            self.place_move(args)
        else:
            self.collapse(args)

    def place_move(self, player, loc1, loc2):
        assert not self.is_win(), "Game already won"
        assert player == 'x' or player == 'o', "not valid symbol for player"
        assert (loc1 not in self.measured) and 1 <= loc1 <= 9, "location to play not on the board"
        assert (loc2 not in self.measured) and 1 <= loc2 <= 9, "location to play not on the board"
        assert not self.cycle
        self.moves += 1
        self.cells[loc1 - 1].add(player + str(self.moves))
        self.cells[loc2 - 1].add(player + str(self.moves))
        self.graph.add_edge(loc1, loc2)

    def collapse(self, player, loc, target_player, move_num):
        assert target_player + str(move_num) in self.cells[loc - 1]
        assert loc not in self.measured
        assert self.cycle
        # TODO: implement collapse dynamics
        self.measured[loc] = target_player

    def detect_cycle(self):
        try:
            self.cycle = nx.find_cycle(self.graph)
        except nx.NetworkXNoCycle:
            return None

    def visualize_entanglement_graph(self):
        # TODO: implement networkx visualization for self.graph
        return