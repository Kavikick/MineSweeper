'''
Filename:
    Start.py
Date last modified:
    May 3, 2019
By:
    Wesley Duerksen
'''

class UI:
    def menu(self):
        import os
        os.system('clear')

        print("Mine Sweeper by Wesley Duerksen")
        print("---------------------------")
        print("New game  = N")
        print("Load game = L")
        print("Quit      = Anything else")
        choice = input(":")

        import Game
        if choice[0] in ['l','L']:
            self.game = Game.Mine_Sweeper()
            self.game.load()
            self.rungame()

        elif choice[0] in ['n','N']:
            self.game = Game.Mine_Sweeper()

            # build the board
            while 1:
                try:
                    width = "empty"
                    height = "empty"
                    user_input = input("Board dimensions [x] [y]: ")
                    user_input = user_input.split(' ')
                    for op in user_input:

                        if op.isdigit() and width == "empty":
                            width = op
                        elif op.isdigit() and height == "empty":
                            height = op

                    if height == "empty" and width == "empty":
                        raise ValueError("Invalid inputs")

                    self.game.build(height,width)
                except ValueError as err:
                    print(err)
                    continue
                break

            percentage = 0
            while 1:
                percentage = input("Bomb percentage (10-80): ")
                if percentage.isdigit():
                    percentage = int(percentage)
                    if percentage >= 10 and percentage <= 80:
                        break
                else:
                    print("bad input")

            # starting square
            self.game.print()
            while 1:
                try:
                    x = "empty"
                    y = "empty"
                    user_input = input("Starting square [x] [y]: ")
                    user_input = user_input.split(' ')
                    for op in user_input:
                        if op.isdigit() and x == "empty":
                            x = op
                        elif op.isdigit() and y == "empty":
                            y = op
                            break

                    if x == "empty" and y == "empty":
                        raise ValueError("Invalid inputs")

                    self.game.base_box(x,y)
                    self.game.put_bombs(percentage)
                    self.game.put_numbers()
                    self.game.reveal()
                except ValueError as err:
                    print(err)
                    continue
                break
            self.rungame()

        print("bye bye")

    def rungame(self):

        # Play
        while self.game.game_status() == "undefined":
            self.game.print()
            print("number of bombs {}".format(self.game.bombs - self.game.num_flagged()))
            print('\nEnter "[operator] [x] [y]"')
            print("Note op isn't needed to run")
            print("To flag op = f")
            print("To unflag  = f")
            print("To save op = s")

            while 1:
                try:
                    user_input = input(">> ")
                    user_input = user_input.split(' ')
                    operator = 'noop'
                    x = "empty"
                    y = "empty"
                    for op in user_input:
                        if op in ['f','F']:
                            operator = 'f'
                        elif op in ['s','S']:
                            self.game.save()
                            return
                            break
                        elif op.isdigit() and x == "empty":
                            x = int(op)
                        elif op.isdigit():
                            y = int(op)
                    self.game.update(x,y,operator)
                except ValueError as err:
                    print(err)
                    continue
                break

        if self.game.game_status() == "won":
            self.game.print()
            print("YOU WIN!!!!!")
        elif self.game.game_status() == "lost":
            self.game.expose()
            self.game.print()
            print("you lost...")
