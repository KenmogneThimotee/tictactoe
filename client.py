from zero import ZeroClient
import tkinter as tk
from tkinter import messagebox
from msgspec import Struct
import sys

zero_client = ZeroClient("localhost", 5559)

current_player = None
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] 

def connect():
    global current_player

    msg =  zero_client.call("connect_player", None)
    print(msg)
    if msg == 2:
        sys.exit(1)
    current_player = msg

    return msg

connect()



window = tk.Tk()
window.title("Tic Tac Toe")

# Create board
def create_board():
    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text="", font=("Arial", 50), height=2, width=6, bg="lightblue", command=lambda row=i, col=j: handle_click(row, col))
            button.grid(row=i, column=j, sticky="nsew")

create_board()

# Handle button clicks

class Position(Struct):
    row: int
    col: int
    current_player: int


def handle_click(row, col):
    
    global current_player, board

    if board[row][col] == 0:
        
        position = Position(row, col, current_player)
        value =  zero_client.call("handle_click", position)
        print("Board ", board)
        if value:
            board = value
            button = window.grid_slaves(row=row, column=col)[0]
            button.config(text=board[row][col])

        # check_for_winner()
        
window.mainloop()