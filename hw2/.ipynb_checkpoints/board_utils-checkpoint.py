import numpy as np


class Board:
    def __init__(self, board_array, g, target_array):
        self.board = board_array
        self.target = target_array
        self.g = g
        self.h = self._get_h_()[0]
        self.f = self.g + self.h

    def _get_h_(self):
        return manhattan(self.board, self.target)
    
    def __repr__(self):
        return f'{self.board}'
    
    def is_target(self):
        return (False not in (self.board == self.target))



def gen_board(n,m):
    board = np.zeros((n,m)).astype(int)
    for i in range(1,(n*m)):
        placed = False
        while not placed:
            x = np.random.choice(range(0,n),1)
            y = np.random.choice(range(0,m),1)
            if board[x,y] == 0:
                board[x,y] = int(i)
                placed = True
    return board


#Heueristic:
def manhattan(b,t):
    distance = 0
    for item in b.ravel():
        if item != 0:
            board_x, board_y = np.where(b == item)
            target_x, target_y = np.where(t == item)

            delta = abs(board_x - target_x) + abs(board_y - target_y)
            distance += delta

    return distance

def get_valid_moves(board):
    empty_x, empty_y = np.where(board == 0)
    x_neighbors = []
    y_neighbors = []
    if (empty_x - 1) >= 0:
        x_neighbors.append(empty_x - 1)
    if (empty_x + 1) <= board.shape[0]-1:
        x_neighbors.append(empty_x + 1)
    if (empty_y - 1) >= 0:
        y_neighbors.append(empty_y - 1)
    if (empty_y + 1) <= board.shape[1]-1:
        y_neighbors.append(empty_y + 1)

    valid_neighbors = [[int(x[0]),int(empty_y)] for x in x_neighbors] + [[int(empty_x),int(y[0])] for y in y_neighbors]
    return valid_neighbors

def where(board, val):
    return [int(i) for i in np.where(board==val)]

def swap(c_1, c_2, board):
    c_1 = tuple(c_1)
    c_2 = tuple(c_2)
    board_copy = board.copy()
    #b,a = a,b
    board_copy[c_2], board_copy[c_1] = board_copy[c_1], board_copy[c_2]
    return board_copy

def pathgen(board, target):
    b = board.board
    t = target.board
    b_g = board.g
    
    empty = where(b, 0)
    moves = get_valid_moves(b)
    board_list = []
    for n in moves:
        board_list.append(Board(swap(n, empty, b), b_g+1, t))
    return board_list