from Board import QBoard
import tkinter as tk


def change_button(number):
    if not number + 1 in board.measured.keys():
        tiles[number].configure(text=", ".join(board.cells[number]))
    else:
        tiles[number].configure(text=board.measured[number + 1])


def changeGameState(pressedButtonNumber):
    if pressedButtonNumber + 1 in board.measured.keys():
        return
    global last_move
    won = board.is_win()
    if board.cycle and not won:
        # Collapse
        print("collapsing")
        nodes = set([i[0] for i in board.cycle] + [i[1] for i in board.cycle])
        last_move = None
        if pressedButtonNumber + 1 in nodes:
            try:
                board.collapse(pressedButtonNumber + 1, collapse.get(), nodes)
            except:
                label.configure(text="Invalid input")
            for i in range(9):
                change_button(i)
    elif not won:
        # Add state
        print("We are registering place move")
        if last_move and last_move != pressedButtonNumber:  # otherwise we need to wait for another turn.
            try:
                board.make_move("place", last_move + 1, pressedButtonNumber + 1)
                change_button(last_move)
                change_button(pressedButtonNumber)
                last_move = None
                label.configure(text="Turn Successful")
                board.detect_cycle(label=label)
            except AssertionError as e:
                print("an error was raised", e)
            return
        last_move = pressedButtonNumber
        label.configure(text="Select another box to complete turn")
    else:
        label.configure(text=f"{won} won")
    print(board)


if __name__ == '__main__':
    display = tk.Tk()
    display.title("Quantum Tic Tac Toe")
    display.grid()
    tiles = []
    for tile_number in range(9):
        curr_btn = tk.Button(display, text="", width="20", height="5", border="2",
                             command=lambda tile_number=tile_number: changeGameState(tile_number))
        curr_btn.grid(row=tile_number // 3, column=tile_number % 3)
        tiles.append(curr_btn)
    label = tk.Label(master=display, text="")
    label.grid(row=3, columnspan=3)
    collapse = tk.Entry(master=display)
    collapse.grid(row=4, columnspan=3)
    board = QBoard()
    last_move = None
    display.mainloop()
