import networkx as nx


class QBoard:
    def __init__(self):
        self.cells = [set() for i in range(9)]
        self.measured = dict()
        self.moves = 0
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(1, 10))
        self.cycle = False
        self.curr_turn = 'x'

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
            result = self.all_same(win_comb)
            if result:
                return result
        return False

    def all_same(self, loc_list):
        contents = {self.measured[loc] if loc in self.measured else -1 for loc in loc_list}
        if -1 in contents:
            return False
        elif len(contents) == 1:
            return contents.pop()
        else:
            return False

    def make_move(self, type, *args):
        assert type == "collapse" or type == "place"
        if type == "place":
            self.place_move(args)
        else:
            self.collapse(args)

        if self.curr_turn == 'x':
            self.curr_turn = 'o'
        if self.curr_turn == 'o':
            self.curr_turn = 'x'

    def place_move(self, loc1, loc2):
        assert not self.is_win(), "Game already won"
        assert self.curr_turn == 'x' or self.curr_turn == 'o', "not valid symbol for player"
        assert (loc1 not in self.measured) and 1 <= loc1 <= 9, "location to play not on the board"
        assert (loc2 not in self.measured) and 1 <= loc2 <= 9, "location to play not on the board"
        assert not self.cycle
        self.moves += 1
        self.cells[loc1 - 1].add(str(self.curr_turn) + str(self.moves))
        self.cells[loc2 - 1].add(str(self.curr_turn) + str(self.moves))
        self.graph.add_edge(loc1, loc2)

    def collapse(self, loc, target_player, move_num):
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
