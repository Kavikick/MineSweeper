import Game
import Start

test = 0
if test:
    test_game = Game.Mine_Sweeper()
    test_game.build(10,10)
    test_game.put_bombs(10)
    test_game.expose()
    test_game.print()
else:
    run = Start.UI()
    run.menu()
