import Minesweeper
game = Minesweeper.Minesweeper()

print(game)
print('\n')
while True:
    lose = game.select_tile()
    win = game.win()
    if win or lose:
        break
    else:
        print(game)
        print('\n')

