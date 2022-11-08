import random
# Helper function to help create the game board
def update_board(tiles):
    board = '  '
    for i in range(len(tiles[0])):
        if i <= 9:
            board += ' ' + str(i+1) + ' '
        else:
            board += str(i+1) + ' '
    for i in range(len(tiles)):
        board += '\n' + str(i + 1)
        if i < 9:
            board += ' '
        for j in range(len(tiles[i])):
            board += '[' + tiles[i][j] + ']'
    return board


class Minesweeper:
    # initializes game where the difficulty selected determines the amount of rows columns and mines 
    def __init__(self, difficulty = 'Easy'):
        self.difficulty = difficulty
        if self.difficulty in ('Easy', 'easy'):
            self.ROWS, self.COLS, self.mines = 9, 9, 10
            
        elif self.difficulty in ('Medium', 'medium'):
            self.ROWS, self.COLS, self.mines = 16, 16, 40

        elif self.difficulty in ('Hard', 'hard'):
            self.ROWS, self.COLS, self.mines = 16, 30, 99
        self.tile_matrix = [[' ' for i in range(self.COLS)] for j in range(self.ROWS)]    # Creates empty matrix that will contain tile placement
        self.guess_matrix = [[' ' for i in range(self.COLS)] for j in range(self.ROWS)]    # Creates empty matrix that will fill in as player makes guesses
        self.board = update_board(self.guess_matrix)    # creates board that will show to players 
        self.flags = self.mines
        self.first_guess = True

    def __str__(self):
        return self.board

    # Randomly generates the positions for the mines and places them into the tile matrix
    def place_mines(self, first_guess = None):
        placement_set = set()
        #Randomly generates indexes for mine placement
        while len(placement_set) < self.mines:
            randRow = random.randint(0, self.ROWS - 1)
            randCol =  random.randint(0, self.COLS - 1)
            if (randRow, randCol) != first_guess:
                placement_set.add((randRow, randCol))
        #Places the mines into the tile matrix at the randomly generated indexes
        for i in range(len(self.tile_matrix)):
            for j in range(len(self.tile_matrix[i])):
                if (i, j) in placement_set:
                    self.tile_matrix[i][j] = '*'
                    
    def generate_tiles(self):
        #Tallies a tiles number of adjacent mines
        for i in range(len(self.tile_matrix)):
            for j in range(len(self.tile_matrix[i])):
                if self.tile_matrix[i][j] != '*':
                    tile_num = 0
                    try:
                        if self.tile_matrix[i-1][j-1] == '*' and i-1 >= 0 and j-1 >= 0:
                            tile_num += 1
                    except IndexError:
                        pass
                    try:
                        if self.tile_matrix[i-1][j] == '*' and i-1 >= 0:
                            tile_num += 1
                    except IndexError:
                        pass                    
                    try:
                        if self.tile_matrix[i-1][j+1] == '*' and i-1 >= 0:
                            tile_num += 1
                    except IndexError:
                        pass
                    try:
                        if self.tile_matrix[i][j-1] == '*' and j-1 >= 0:
                            tile_num += 1
                    except IndexError:
                        pass
                    try:
                        if self.tile_matrix[i][j+1] == '*':
                            tile_num += 1
                    except IndexError:
                        pass
                    try:
                        if self.tile_matrix[i+1][j-1] == '*' and j-1 >= 0:
                            tile_num += 1
                    except IndexError:
                        pass
                    try:
                        if self.tile_matrix[i+1][j] == '*':
                            tile_num += 1
                    except IndexError:
                        pass                    
                    try:
                        if self.tile_matrix[i+1][j+1] == '*':
                            tile_num += 1
                    except IndexError:
                        pass

                    self.tile_matrix[i][j] = str(tile_num)

            
        
    def reveal_zero_neighbors(self, row, col, checked_set = set()):
        if row < 0 or col < 0:
            return
        try:
            self.tile_matrix[row][col]
        except IndexError:
            pass
        else:
            if (row, col) in checked_set:
                return
            else:
                checked_set.add((row, col))
                if self.tile_matrix[row][col] != '0':
                    self.guess_matrix[row][col] = self.tile_matrix[row][col]
                    return
                else:
                    self.guess_matrix[row][col] = self.tile_matrix[row][col]
                    self.reveal_zero_neighbors(row - 1, col - 1)
                    self.reveal_zero_neighbors(row - 1, col)
                    self.reveal_zero_neighbors(row - 1, col + 1)
                    self.reveal_zero_neighbors(row, col - 1)
                    self.reveal_zero_neighbors(row, col + 1)
                    self.reveal_zero_neighbors(row + 1, col - 1)
                    self.reveal_zero_neighbors(row + 1, col)
                    self.reveal_zero_neighbors(row + 1, col + 1)
                    return


    def select_tile(self):
        while True:
            guess = input('Specify a guess r, c or input F/f to place or unplace a flag: ')
            # Places a flag at designated tile instead of making a guess
            if guess in ('F', 'f'):   
                flag = input('Specify a flag placement r, c: ')
                try:
                    r, c = tuple(flag.strip().split(','))
                except:
                    print('Response should be r, c. Try again! \n')
                else:
                    try:
                        r, c = int(r)-1, int(c)-1
                    except ValueError:
                        print('R and c should be whole numbers. Try again!\n')
                    else:
                        if r in range(len(self.guess_matrix)) and c in range(len(self.guess_matrix[1])) and self.guess_matrix[r][c] == ' ':
                            if self.flags > 0:
                                self.guess_matrix[r][c] = 'F'
                                self.board = update_board(self.guess_matrix)
                                self.flags -= 1
                                print('Flags remaining:', self.flags)
                                return False
                            else:
                                print('No more flags!')
                        elif r in range(len(self.guess_matrix)) and c in range(len(self.guess_matrix[1])) and self.guess_matrix[r][c] == 'F':
                            self.guess_matrix[r][c] = ' '
                            self.board = update_board(self.guess_matrix)
                            self.flags += 1
                            print('Flags remaining:', self.flags)
                            return False                        
                        else:
                            print('Illegal move specified. Try again! \n')
                                
            else:
                try:
                    r, c = tuple(guess.strip().split(','))
                except:
                    print('Response should be r, c. Try again!\n')
                else:
                    try:
                        r, c = int(r)-1, int(c)-1
                    except ValueError:
                        print('R and c should be whole numbers. Try again!\n')
                    else:
                        if self.first_guess:
                            self.place_mines((r, c))
                            self.generate_tiles()
                            self.first_guess = False
                        if r in range(len(self.guess_matrix)) and c in range(len(self.guess_matrix[1])) and self.guess_matrix[r][c] == ' ':
                            if self.tile_matrix[r][c] == '*':
                                self.lose()
                                return True

                            elif self.tile_matrix[r][c] == '0':
                                self.reveal_zero_neighbors(r, c)
                                self.board = update_board(self.guess_matrix)
                                return False
                            else:
                                self.guess_matrix[r][c] = self.tile_matrix[r][c]
                                self.board = update_board(self.guess_matrix)
                                return False
            
                        else:
                            print('Illegal move specified. Try again!\n')

    def lose(self):
        for i in range(len(self.tile_matrix)):
            for j in range(len(self.tile_matrix[i])):
                if self.tile_matrix[i][j] == '*':
                    self.guess_matrix[i][j] = self.tile_matrix[i][j]
        self.board = update_board(self.guess_matrix)
        print(self.board)
        print('\n')
        print('Sorry! You lost.')


    def win(self):
        for i in range(len(self.guess_matrix)):
            for j in range(len(self.guess_matrix[i])):
                if self.tile_matrix[i][j] != '*' and self.guess_matrix[i][j] == ' ':
                    return False
        for i in range(len(self.guess_matrix)):
            for j in range(len(self.guess_matrix[i])):
                if self.tile_matrix[i][j] == '*' and self.guess_matrix[i][j] != 'F':
                    self.guess_matrix[i][j] = 'F'
        self.board = update_board(self.guess_matrix)
        print(self.board)
        print('\n')
        print('Congrats! You won!')
        return True
