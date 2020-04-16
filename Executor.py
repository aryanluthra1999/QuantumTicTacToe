from GameState import GameState
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx

def change_button(number):
    print("changing state with ", number)
    tiles[number].configure(text=", ".join(state.board.cells[number]))

def changeGameState(pressedButtonNumber):
        global last_move
        print(f"last move {last_move} and curr {pressedButtonNumber}")
        cycles = state.board.detect_cycle()
        won = False #state.board.is_win()
        if cycles and not won:
            # Collapse
            pass
        elif not won:
            # Add state
            print("no cycles")
            if last_move and last_move != pressedButtonNumber: #otherwise we need to wait for another turn.
                try:
                    state.board.make_move("place", last_move + 1, pressedButtonNumber + 1)
                    change_button(last_move)
                    change_button(pressedButtonNumber)
                    last_move = None
                except AssertionError as e:
                    print("an error was raised", e)
                return
            last_move = pressedButtonNumber


if __name__ == '__main__':
    matplotlib.use("TkAgg")
    display = tk.Tk()
    display.title("Quantum Tic Tac Toe")
    display.grid()
    tiles = []
    for tile_number in range(9):
        curr_btn = tk.Button(display, text="", width="20",height="5", border="2",
        command=lambda tile_number = tile_number: changeGameState(tile_number))
        curr_btn.grid(row=tile_number//3, column=tile_number%3)
        tiles.append(curr_btn)
    state = GameState()
    nx.draw(state.board.graph)
    last_move = None
    display.mainloop()
