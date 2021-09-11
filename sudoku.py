def find_next_empty(puzzle):
    # returns the next row,col of the puzzle that is empty (represented by 0)

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return row, col
    return None, None

def valid_guess(puzzle, guess, row, col):
    # checks validity of the guess returns True/False

    # check row
    vals_row = puzzle[row]
    if guess in vals_row:
        return False

    # check column
    for i in range(9):
        if guess == puzzle[i][col]:
            return False
    
    # check the surrounding 3x3 matrix
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if guess == puzzle[r][c]:
                return False 

    return True
    

def solve(puzzle):
    # solve sudoku using backtracking 
    # returns True is solutions exists and false otherwise
    # solves puzzle and returns puzzle if solution exists

    # Step 1: choose next place on puzzle to make a guess/end game
    row, col = find_next_empty(puzzle)

    if row is None: 
        return True 

    # Step 2: make a guess/check if valid guess
    for guess in range(1, 10):
        if valid_guess(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve(puzzle):
                return True

        # if not valid OR our guess doe not solve the puzzle, must backtrack and try new number
        puzzle[row][col] = 0

    # if none of the numbers work then puzzle is unsolvable
    return False


if __name__ == '__main__':
    board = [
        [0, 0, 0, 0, 0 ,0, 6, 0, 9],
        [1, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 5, 3, 0, 6, 8, 2, 1], 
        [0, 0, 4, 6, 7, 0, 0, 5, 0],
        [0, 0, 7, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 5, 4, 0, 0, 0, 0],
        [3, 7, 0, 4, 0, 5, 2, 0, 6],
        [0, 0, 0, 0, 0, 0, 5, 1, 0],
        [0, 6, 0, 0, 2, 0, 0, 3, 7]            
    ]
    print(solve(board))
    print(board)


