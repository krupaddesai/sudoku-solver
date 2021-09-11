from sudoku import find_next_empty
import pygame
import requests

WIDTH = 550
background_color = (255,255,255)
text_color = (32,99,155)

puzzle = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = puzzle.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
buffer = 5

def insert(window, position):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Roboto', 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(window, (pos[0]//50, pos[1]//50))
                return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i - 1][j - 1] != 0):
                    return
                if event.key == pygame.K_DELETE: #check for 0 input
                    pygame.draw.rect(window, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                    return
                if (0 < event.key - 48 < 10): #check for valid input
                    pygame.draw.rect(window, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    value = myfont.render(str(event.key - 48), True, (89,166,180))
                    window.blit(value, (position[0]*50 + 18, position[1]*50 + 11))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return    
                return

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
    

def solve(window, grid):
    myfont = pygame.font.SysFont('Roboto', 50)
    # solve sudoku using backtracking 
    # returns True is solutions exists and false otherwise
    # solves puzzle and returns puzzle if solution exists

    # Step 1: choose next place on puzzle to make a guess/end game
    row, col = find_next_empty(grid)

    if row is None: 
        return True 

    # Step 2: make a guess/check if valid guess
    for guess in range(1, 10):
        if valid_guess(grid, guess, row, col):
            grid[row][col] = guess
            value = myfont.render(str(guess), True, (89,166,180))
            pygame.draw.rect(window, background_color, ((col + 1)*50 + buffer, (row+1)*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
            window.blit(value, ((col+1)*50 + 18, (row+1)*50 + 11))
            pygame.display.update()
            pygame.time.delay(10)
            if solve(window, grid):
                return True

        # if not valid OR our guess doe not solve the puzzle, must backtrack and try new number
        grid[row][col] = 0
        pygame.draw.rect(window, background_color, ((col + 1)*50 + buffer, (row+1)*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
        pygame.display.update()

    # if none of the numbers work then puzzle is unsolvable
    return False

            
def main():
    pygame.init()
    window = pygame.display.set_mode(size=(WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    window.fill((148,119,139))
    myfont = pygame.font.SysFont('Roboto', 50)
    
    pygame.draw.rect(window, (255,255,255), (50,50, 450,450))
    pygame.display.update()

    # create grid
    for i in range(0,10):
        if i % 3 == 0:
            pygame.draw.line(window,(23,63,95), (50+50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(window,(23,63,95), (50, 50+50*i), (500, 50+50*i), 4)

        pygame.draw.line(window,(23,63,95), (50+50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(window,(23,63,95), (50, 50+50*i), (500, 50+50*i), 2)

    pygame.display.update()

    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if (0 < grid[i][j] < 10):
                value = myfont.render(str(grid[i][j]), True, text_color)
                window.blit(value, ((j+1)*50 + 17, (i+1)*50 + 12) )
    pygame.display.update()

    



    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(window, (pos[0]//50, pos[1]//50))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solve(window, grid_original)
            if event.type == pygame.QUIT:
                pygame.quit()
                return 

main()
