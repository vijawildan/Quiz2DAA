# import library
import random
import re

class Board:
    def __init__(self, dimension, num_bombs):
        self.dimension = dimension
        self.num_bombs = num_bombs

        # to make board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initalize set to keep track of locations uncovered
        self.dug = set() 

    # construct a new board based on dimension and the total of the bombs
    def make_new_board(self):
        
        # generate a new board
        board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        
        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dimension**2 - 1) 
            row = loc // self.dimension  
            col = loc % self.dimension  

            # function to determine if the bomb already planted. If it is, it will keep going
            if board[row][col] == '*':
                continue
            
            # to plant the bombs
            board[row][col] = '*' 
            bombs_planted += 1

        return board

    # assigning a number for the empty space to represent how much bombs there are
    def assign_values_to_board(self):
        for r in range(self.dimension):
            for c in range(self.dimension):

                # if it's a bomb, it don't have to calculate
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_get_nearby_bombs(r, c)

    def get_get_nearby_bombs(self, row, col):
        get_nearby_bombs = 0
        for r in range(max(0, row-1), min(self.dimension-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimension-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    get_nearby_bombs += 1

        return get_nearby_bombs

    # digging the location
    def dig(self, row, col):
        
        # to keep track if we dig here
        self.dug.add((row, col)) 
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dimension-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimension-1, col+1)+1):
                
                # not digging, place already dug
                if (r, c) in self.dug:
                    continue 
                self.dig(r, c)

        return True

    # to return a string that shows the board
    def __str__(self):
        
        # new array that represent what we would see
        visible_board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        for row in range(self.dimension):
            for col in range(self.dimension):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put together in a string
        string_rep = ''

        #to get the max columns widths for printing
        widths = []
        for idx in range(self.dimension):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the string
        indices = [i for i in range(self.dimension)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dimension)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# play the game
def play(dimension=10, num_bombs=10):
    board = Board(dimension, num_bombs)

    safe = True 

    while len(board.dug) < board.dimension ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dimension or col < 0 or col >= dimension:
            print("Invalid location. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            break 

    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        board.dug = [(r,c) for r in range(board.dimension) for c in range(board.dimension)]
        print(board)

if __name__ == '__main__': 
    play()