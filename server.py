from zero import ZeroServer
from msgspec import Struct
from typing import Union

app = ZeroServer(port=5559)

class Parameter:

    def __init__(self) -> None:
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_0 = False
        self.player_1 = False
        self.previous_player = None
        
    
    def update_player_1(self, value):
        self.player_1 = value
    
    def update_player_0(self, value):
        self.player_0 = value
    
params = Parameter()

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
player_0 = False
player_1 = False
previous_player = 0
start_player = 0



class Position(Struct):
    row: int
    col: int
    current_player: int


@app.register_rpc
async def connect_player() -> int:
            
    print(params.player_0, params.player_1)
    
    if not params.player_0:
        params.update_player_0(True)
        return 0
    elif not params.player_1:
        params.update_player_1(True) 
        return 1
    else:
        return 2

# Handle button clicks
@app.register_rpc
async def handle_click(position: Position) -> Union[list, None]:
    
    global previous_player, start_player
    
    print("Previous Player: ", previous_player, start_player)

    if params.board[position['row']][position['col']] == 0:
        if (position['current_player'] == 0 and previous_player != 0) or start_player == 0:
            params.board[position['row']][position['col']] = "X"
            previous_player = 0
            start_player = 1
        elif position['current_player'] == 1 and previous_player != 1:
            params.board[position['row']][position['col']] = "O"
            previous_player = 1
        else:
            return None
        
        return params.board
    return None

# Check for a winner or a tie
@app.register_rpc
async def check_for_winner() -> str:
    winner = None

    # Check rows
    for row in params.params.board:
        if row.count(row[0]) == len(row) and row[0] != 0:
            winner = row[0]
            break

    # Check columns
    for col in range(len(params.params.board)):
        if params.params.board[0][col] == params.board[1][col] == params.board[2][col] and params.board[0][col] != 0:
            winner = params.board[0][col]
            break

    # Check diagonals
    if params.board[0][0] == params.board[1][1] == params.board[2][2] and params.board[0][0] != 0:
        winner = params.board[0][0]
    elif params.board[0][2] == params.board[1][1] == params.board[2][0] and params.board[0][2] != 0:
        winner = params.board[0][2]

    if all([all(row) for row in params.board]) and winner is None:
        winner = "tie"

    return winner
        


if __name__ == "__main__":
    
    app.run()
