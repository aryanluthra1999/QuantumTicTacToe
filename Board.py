import networkx as nx
import random
from itertools import combinations
from copy import deepcopy


class QBoard:
    def __init__(self, alg=True):
        self.check = random.randint(1, 1000)
        self.cells = [set() for i in range(9)]
        self.measured = dict()
        self.moves = 0
        self.graph = nx.MultiGraph()
        self.graph.add_nodes_from(range(1, 10))
        self.cycle = None
        self.curr_turn = 'x'
        self.move_locs = dict()
        self.alg = alg

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
        if len(self.measured) == 9:
            return "nobody"
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

        self.detect_cycle()
        # print(self)    
        
        assert type == "collapse" or type == "place"
        if type == "place":
            self.place_move(*args)
        else:
            self.collapse(*args)

        self.detect_cycle()

        if not self.cycle:
            if self.curr_turn == 'x':
                self.curr_turn = 'o'
                # print("Switching Turns")
            elif self.curr_turn == 'o':
                self.curr_turn = 'x'
                # print("Switching Turns")
                if self.alg:
                    print(self.minimax())
            else:
                assert self.curr_turn == 'x' or self.curr_turn == 'o', "not valid symbol for player"
        else:
            if self.curr_turn == 'x' and self.alg:
                print(self.minimax())


    def place_move(self, loc1, loc2):
        assert not self.is_win(), "Game already won"
        assert self.curr_turn == 'x' or self.curr_turn == 'o', "not valid symbol for player"
        assert (loc1 not in self.measured) and 1 <= loc1 <= 9, "location to play not on the board"
        assert (loc2 not in self.measured) and 1 <= loc2 <= 9, "location to play not on the board"
        assert self.cycle is None
        
        self.moves += 1
        move_str = str(self.curr_turn) + str(self.moves)
        self.cells[loc1 - 1].add(move_str)
        self.cells[loc2 - 1].add(move_str)
        self.graph.add_edge(loc1, loc2)
        self.move_locs[move_str] = (loc1, loc2)

        self.detect_cycle()

    def collapse(self, loc, move_str, nodes):
        assert move_str in self.cells[loc - 1]
        assert loc not in self.measured
        assert loc in nodes
        assert self.move_locs[move_str][0] in nodes and self.move_locs[move_str][1] in nodes
        assert self.cycle

        self.collapse_helper(loc, move_str)

        for loc in self.measured:
            if loc in self.graph.nodes:
                self.graph.remove_node(loc)
                self.cells[loc - 1] = set()

        for cell in self.cells:
            if move_str in cell:
                cell.remove(move_str)

        self.detect_cycle()

        if self.curr_turn == 'x':
            self.curr_turn = 'o'
            # print("Switching Turns")
        elif self.curr_turn == 'o':
            self.curr_turn = 'x'
            # print("Switching Turns")
            if self.alg:
                print(self.minimax())

    def collapse_helper(self, loc, move_str):

        self.measured[loc] = move_str[0].upper()
        # TODO: implement collapse dynamics
        self.cells[loc - 1].remove(move_str)

        for other_move in self.cells[loc - 1]:
            if other_move == move_str or other_move in self.measured.values():
                continue
            for other_loc in self.move_locs[other_move]:
                if other_loc not in self.measured:
                    self.collapse_helper(other_loc, other_move)

    def detect_cycle(self, label=None):
        try:
            self.cycle = nx.find_cycle(self.graph)
            if label:
                label.configure(text="You will now have to collapse the system"
                                     + " \n enter the item u want to measure and click the block")
        except nx.NetworkXNoCycle:
            self.cycle = None

    def __str__(self):
        result = "### THE CURRENT BOARD ### \n"
        result += str(self.check)
        result += "\n CURRENT TURN: " + str(self.curr_turn)
        result += "\n MEASURED SQUARES: " + str(self.measured)
        result += "\n CYCLE" + str(self.cycle)
        result += "\n CELLS" + str([str(c) for c in self.cells])
        result += "\n NODES: " + str(self.graph.nodes)
        return result

    def duplicate(self):
        newboard = deepcopy(self)
        newboard.alg = False
        return newboard

    ##### Part 2: Minimax algorithm ####

    def get_succesors(self):
        # TODO: Returns the succesor of the current game state
        assert not self.is_win(), "Game already won, No successors to find. Won by " + str(self.is_win())
        if self.cycle:
            return self.get_collapse_succesors()
        else:
            return self.get_place_succesors()

    def get_place_succesors(self):
        # TODO: Helper method of get succesors in order to get all the succersor when the turn is a place turn
        open_squares = [i for i in range(1, 10) if i not in self.measured.keys()]
        possible_moves = combinations(open_squares, 2)
        succesors = []
        for move in possible_moves:
            new_board = self.duplicate()
            new_board.make_move('place', *move)
            succesors.append((new_board, 'place ' + str(move)))
        return succesors

    def get_collapse_succesors(self):
        # TODO Helper method to get succesors for the collapse turns
        possible_locs = set([i[0] for i in self.cycle] + [i[1] for i in self.cycle])
        possible_moves = dict()
        for loc in possible_locs:
            curr_loc_collapse_moves = []
            for move_str in self.cells[loc - 1]:
                move_str_locs = self.move_locs[move_str]
                if move_str_locs[0] in possible_locs and move_str_locs[1] in possible_locs:
                    curr_loc_collapse_moves.append(move_str)

            possible_moves[loc] = curr_loc_collapse_moves

        # Now adding coppies of the boards as the successors using the possible moves
        successors = []
        for loc, moves in possible_moves.items():
            for move_str in moves:
                new_board = self.duplicate()
                new_board.make_move("collapse", loc, move_str, possible_locs)
                successors.append((new_board, "collapse" + str(loc) + str(move_str)))
        return successors

    @staticmethod
    def utility(board, player, depth):
        winner = board.is_win()
        if winner:
            if winner == "nobody":
                return (0, "tie")
            elif winner == player.upper():
                return (100, player + "win")
            elif winner != player:
                return (-100, player + "loss")
        else:
            # TODO: return utility over succesors here
            if depth > 2:
                return (0, "unknown")
            if depth%2==0:
                ret_util = float("-inf")
            if depth%2==1:
                ret_util = float("inf")
            ret_util_successor_move = None
            #print(depth)
            for successor_board, successor_move in board.get_succesors():
                successor_util = 0.75*(QBoard.utility(successor_board, player, depth + 1)[0])
                if depth%2==0:
                    if successor_util > ret_util:
                        ret_util = successor_util
                        ret_util_successor_move = successor_move
                if depth%2==1:
                    if successor_util < ret_util:
                        ret_util = successor_util
                        ret_util_successor_move = successor_move

            return (ret_util, ret_util_successor_move)
            # return max([utility(succ)-1 for succ,succ_moves in board.get_succesors())]#sub 1 to end game in the least amt moves

    def minimax(self):
        # get successor with the max util
        return QBoard.minimax_helper(self, 4, True, float('-inf'), float('inf'))

    def utility_maxer(board, depth):
        winner = board.is_win()
        if winner == 'X':
            return (100, "win")
        elif winner == 'O':
            return (-100, "loss")
        elif winner == "nobody":
            return (0, "tie")
        else:
            # TODO: return utility over succesors here
            if depth > 4:
                return (0, "unknown")

    @staticmethod
    def minimax_helper(board, depth, isMaximizingPlayer, alpha, beta):

        print(depth)

        winner = board.is_win()
        if winner == 'X':
            return 100, "win"
        elif winner == 'O':
            return -100, "loss"
        elif winner == "nobody":
            return 0, "tie"
        elif depth <= 0:
            measured_vals = board.measured.values()
            num_x = sum([1 for val in measured_vals if val == 'X'])
            num_o = len(measured_vals) - num_x
            return num_x - num_o, "unknown"

        if isMaximizingPlayer:
            bestVal = float('-inf')
            bestMove = None
            for successor_board, successor_move in board.get_succesors():
                value = QBoard.minimax_helper(successor_board, depth - 1, successor_board.curr_turn == 'x', alpha, beta)[0]
                if value > bestVal:
                    bestVal = value
                    bestMove = successor_move
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
            return bestVal, bestMove

        else:
            bestVal = float('inf')
            bestMove = None
            for successor_board, successor_move in board.get_succesors():
                value = QBoard.minimax_helper(successor_board, depth - 1, successor_board.curr_turn == 'x', alpha, beta)[0]
                if value < bestVal:
                    bestVal = value
                    bestMove = successor_move
                beta = min(beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal, bestMove
