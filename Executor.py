from GameState import GameState
import tkinter as tk

def change_button(number, new_value):
    tiles[number].configure(text=new_value)

def changeGameState(pressedButtonNumber):
    # change the GameState
    # Get the last change
    change_button(pressedButtonNumber, "kavi")
    pass

if __name__ == '__main__':
    display = tk.Tk()
    display.title("Quantum Tic Tac Toe")
    display.grid()
    tiles = []
    for tile_number in range(9):
        curr_btn = tk.Button(display, text="", width="20",height="2", border="2",
        command=lambda tile_number = tile_number: changeGameState(tile_number))
        curr_btn.grid(row=tile_number%3, column=tile_number//3)
        tiles.append(curr_btn)

    display.mainloop()
