'''
Filename:
    Game.py
Date last modified:
    May 3, 2019
By:
    Wesley Duerksen
'''

class Mine_Sweeper:

    def build(self,height,width):
        '''
        def:
            makes the game board and fills it
        input:
            height = board Y
            width = board X
        '''
        height = int(height)
        width = int(width)

        # error checking
        input = str(height)+str(width)
        if not input.isdigit():
            raise ValueError("one of the inputs isn't a digit")
        elif 6 > height or height > 100:
            raise ValueError("Invalid Height")
        elif 6 > width or width > 100:
            raise ValueError("Invalid Width")

        # saving the variables
        self.height = int(height)
        self.width = int(width)
        self.board = []

        # create the board
        for i in range(width):
            temp = []
            for k in range(height):
                temp.append("he")
            self.board.append(temp)

    def base_box(self,x,y):
        '''
        def:
            reveal the 3x3 around the first pick
        '''
        x = int(x)-1
        y = int(y)-1

        # error checking
        temp = str(x)+str(y)
        if not temp.isdigit():
            raise ValueError("invalid starting cell")
        elif x < 0 or x > self.width:
            raise ValueError("x out of range")
        elif y < 0 or y > self.height:
            raise ValueError("y out of range")

        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i < 0 or i >= self.width:
                    continue
                elif j < 0 or j >= self.height:
                    continue
                else:
                    self.board[i][j] = 'e'

    def print(self):
        '''
        def:
            prints the board
        '''
        import os
        os.system('clear')

        # top row
        col = 1
        print("  |", end = '')
        for i in range(self.height):
            print("{:^3}".format(str(col)), end = '')
            col += 1
        print("\n---", end = '')
        for i in range(self.height):
            print("---", end = '')
        print('')

        # middle rows
        rows = 1
        for row in self.board:
            # side bar
            if rows < 10:
                print("{:>2}".format(str(rows))+'|', end = '')
            else:
                print(str(rows)+'|', end = '')

            # center
            for box in row:
                if box[0] == 'h':
                    print(" █ ",end = '')
                elif box == 'e':
                    print("   ", end = '')
                elif box == 'b':
                    print(" B ", end = '')
                elif box[0] == 'f':
                    print(" F ", end = '')
                elif box.isdigit():
                    print(" "+box+" ", end = '')
                else:
                    print(box, end = '')

            print('')
            print('')
            rows += 1

        # bottom line
        for i in range(self.height+1):
            print("---", end = '')
        print('')

    def put_bombs(self,percent):
        '''
        pre:
            percent is a whole number between 10 and 80
        post:
            the board is populated with bombs
        '''
        # input checking
        percent = int(percent)
        if not str(percent).isdigit() or 10 > percent or percent > 80:
            raise ValueError("Bad percent")

        import random

        bomb_count = 0
        self.bombs = round(self.width*self.height*percent/100)
        col = 0
        row = 0
        while bomb_count < self.bombs:
            if self.board[col][row] == "he":
                # decide fate
                if random.randint(1,100) < percent:
                    self.board[col][row] = "hb"
                    bomb_count += 1

            # counter manager
            col += 1
            if col == self.width:
                col = 0
                row += 1
            if row == self.height:
                row = 0

    def scan_nearby_cells_for_bomb(self,x,y):
        '''
        return:
            number of bombs in 3x3 to (x,y)
        '''
        count = 0
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i < 0 or i >= self.width:
                    continue
                elif j < 0 or j >= self.height:
                    continue
                elif self.board[i][j] in ["hb","b"]:
                    count += 1

        return count

    def put_numbers(self):
        '''
        def:
            puts in hidden numbers for all the local bombs
        '''
        for x in range(self.width):
            for y in range(self.height):

                if self.board[x][y] != "hb":
                    count = self.scan_nearby_cells_for_bomb(x,y)
                    if count != 0:
                        if self.board[x][y] == 'e':
                            self.board[x][y] = str(count)
                        else:
                            self.board[x][y] = 'h'+str(count)

    def reveal(self):
        '''
        def:
            refreshes the board, revealing all the now exposed empty cells
        '''
        something_changed = 1
        while something_changed:
            something_changed = 0

            for x in range(self.width):
                for y in range(self.height):

                    # skip unnecesary cells
                    if self.board[x][y] in ['b','hb','e','1','2','3','4','5','6','7','8'] or self.board[x][y][0] == 'f':
                        continue
                    else:
                        # compile all cells adjacent
                        cells = []
                        for i in range(x-1,x+2):
                            for j in range(y-1,y+2):
                                if i == x and j == y:
                                    continue
                                else:
                                    cells.append([i,j])

                        # look for edges in sides
                        for i in range(len(cells)):
                            if cells[i][0] < 0 or cells[i][0] >= self.width:
                                cells[i] = "edge"
                            elif cells[i][1] < 0 or cells[i][1] >= self.height:
                                cells[i] = "edge"

                        # load the values that aren't edges
                        for i in range(len(cells)):
                            if cells[i] != "edge":
                                cells[i] = self.board[cells[i][0]][cells[i][1]]

                        # If it has no 'e' neighbors skip it.
                        if 'e' not in cells:
                            continue


                        # reveal the cell
                        self.board[x][y] = self.board[x][y][1]
                        something_changed = 1

    def expose(self):
        '''
        def:
            exposes all of the mines for the user to see.
            all the flagged bombs get a special symbol
        '''
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] in ["hb","fb"]:
                    self.board[x][y] = self.board[x][y][1]

    def update(self,x,y,op):
        '''
        def:
            reveals or flags the (x,y) cell
            updates the rest of the board if a cell was revealed
        input:
            op = default no-op, if 'flag' flags cell
            x = x cord assuming not base 0
            y = y cord assuming not base 0
        note:
            all the dimensions are twisted around because the person see's the board flipped
        '''
        x = int(x)-1
        y = int(y)-1

        # input checker
        if not str(x).isdigit():
            raise ValueError("Invalid x input")
        elif not str(y).isdigit():
            raise ValueError("Invalid y input")
        elif x < 0 or x >= self.height or y < 0 or y >= self.width:
            raise ValueError("Cell out of range")
        elif self.board[y][x].isdigit() or self.board[y][x] == 'e':
            raise ValueError("Fhat cell is already revealed")

        # flagging the cell or revealing it
        if op == 'f':
            if self.board[y][x][0] == 'f':
                self.board[y][x] = 'h'+self.board[y][x][1]
            else:
                self.board[y][x] = 'f'+self.board[y][x][1]
        else:
            self.board[y][x] = self.board[y][x][1]
            self.reveal()

    def save(self):
        '''
        def:
            saves board in csv form
        input:
            filename = what to name the file
            time = the current run time
        '''
        import csv
        with open("savegame.txt",'w') as file:
            csv_file = csv.writer(file,delimiter = ',')
            csv_file.writerow([self.width,self.height,self.bombs])
            for row in self.board:
                csv_file.writerow(row)

    def load(self):
        '''
        def:
            builds a board from a file
        '''
        data = []
        import csv
        with open('savegame.txt','r') as file:
            csv_file = csv.reader(file,delimiter = ',')
            for row in csv_file:
                data.append(row)

        # getting necessary variables
        self.width = int(data[0][0])
        self.height = int(data[0][1])
        self.bombs = int(data[0][1])

        # copying the rest
        self.board = []
        for i in range(1,len(data)):
            self.board.append(data[i])

    def game_status(self):
        '''
        def:
            Determines the status of the game
        post:
            returns string indicating if the game is won, lost, undefined
        '''
        # is a bomb exposed
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == "b":
                    return "lost"
        # all bombs aren't flagged
        flagged = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y][0] == 'f':
                    cell = self.board[x][y][1]
                    if cell.isdigit() or cell == 'b':
                        flagged += 1
        if flagged != self.bombs:
            return "undefined"
        # if those failed
        return "won"

    def num_flagged(self):
        '''
        returns the number of flagged
        '''
        count = 0
        for row in self.board:
            for cell in row:
                if cell[0] == 'f':
                    count += 1
        return count
