import Game

for i in range(5,100):
    print(i)
    game_test = Game.Mine_Sweeper()
    game_test.build(i,i,4,4,20)
    try:
        game_test.update(0,0)
    except ValueError as err:
        print(err)

    #game_test.save()
    #game_test.load()
