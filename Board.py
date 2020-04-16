import networkx as nx
import random


class QBoard:
    def __init__(self):
        self.check = random.randint(1, 1000)
        self.cells = [set() for i in range(9)]
        self.measured = dict()
        self.moves = 0
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(1, 10))
        self.cycle = None
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
        print(self)
        assert type == "collapse" or type == "place"
        if type == "place":
            self.place_move(*args)
        else:
            self.collapse(*args)

        self.detect_cycle()
        if not self.cycle:
            if self.curr_turn == 'x':
                self.curr_turn = 'o'
                print("Switching Turns")
            elif self.curr_turn == 'o':
                self.curr_turn = 'x'
                print("Switching Turns")
            else:
                assert self.curr_turn == 'x' or self.curr_turn == 'o', "not valid symbol for player"

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

    def collapse(self, loc, move_str):
        assert move_str in self.cells[loc - 1]
        assert loc not in self.measured
        assert self.cycle
        self.measured[loc] = move_str[0]

        # TODO: implement collapse dynamics

        for loc in self.measured:
            if loc in self.graph.nodes:
                self.graph.remove_node(loc)
                self.cells[loc-1] = set()

        for cell in self.cells:
            if move_str in cell:
                cell.remove(move_str)

        self.detect_cycle()

    def detect_cycle(self, label=None):
        try:
            self.cycle = nx.find_cycle(self.graph)
            if label:
                label.configure(text="You will now have to collapse the system"
                + " enter the item u want to measure and click the block")
        except nx.NetworkXNoCycle:
            self.cycle = None

    def visualize_entanglement_graph(self):
        # TODO: implement networkx visualization for self.graph
        return

    def __str__(self):
        result = "### THE CURRENT BOARD ### \n"
        result += str(self.check)
        result += "CURRENT TURN: " + str(self.curr_turn)
        result += "MEASURED SQUARES: " + str(self.measured)
        return result
