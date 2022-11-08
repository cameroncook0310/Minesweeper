import Minesweeper

def main():
    while True:
        while True:
            difficulty = input('What difficulty would you like to play (easy, medium, hard)?: ')
            if difficulty in('Easy', 'easy', 'Medium', 'medium', 'Hard', 'hard'):
                game = Minesweeper.Minesweeper(difficulty)
                print(game)
                print('\n')
                break
            else:
                print('Please enter a valid difficulty.')
            
        while True:
            lose = game.select_tile()
            win = game.win()
            if win or lose:
                break
            else:
                print(game)
                print('\n')
        new_game = input('If you would like to play another game input Y/y, or input any other key to stop playing: ')
        print('\n')
        if new_game not in ('Y', 'y'):
            break

main()
