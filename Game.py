class Mine_Sweeper:
    #def __init__:

    def build(self,height,width,x,y,percent):
        '''
        def:
            makes the game board and fills it
        input:
            height = board Y
            width = board X
            x = Starting square's x cord
            y = Starting square's y cord
            percent = whole number between 10-80
        '''
        self.height = height
        self.width = width
        self.board = []

        # create the board
        for i in range(width):
            temp = []
            for k in range(height):
                temp.append("he")
            self.board.append(temp)

        # fill the board
        self.base_box(x,y)
        self.put_bombs(percent)
        self.put_numbers()
        self.reveal()

    def base_box(self,x,y):
        '''
        def:
            reveal the 3x3 around the first pick
        '''
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
        # top bar
        for i in range(self.width):
            print("---", end = '')
        print('')

        # middle rows
        for row in self.board:
            #print('|', end = '')
            for box in row:
                if box[0] == 'h':
                    print(" \ ",end = '')
                elif box == 'e':
                    print("   ", end = '')
                elif box == 'b':
                    print(" X ", end = '')
                elif box[0] == 'f':
                    print(" F ", end = '')
                else:
                    print(" "+box+" ", end = '')
            print('')
        # ⬜☢⬛

        # bottom bar
        for i in range(self.width):
            print("---", end = '')
        print('')

    def put_bombs(self,percent):
        '''
        pre:
            percent is a whole number between 10 and 80
        post:
            the board is populated with bombs
        '''
        import random

        bomb_count = 0
        target = round(self.width*self.height*percent/100)
        col = 0
        row = 0
        while bomb_count < target:
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

    def scan_nearby_cell(self,x,y):
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
                    count = self.scan_nearby_cell(x,y)
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
            # loop through all columns
            something_changed = 0
            for x in range(self.width):
                # loop through all rows
                for y in range(self.height):
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

                        # reveal if sides = 'e'
                        edges_worked ="no"
                        for i in [1,3,4,6]:
                            if cells[i] == 'e':
                                self.board[x][y] = self.board[x][y][1]
                                something_changed = 1
                                edges_worked = "yes"
                                break
                        # check all edge corner combos
                        if edges_worked == "no":
                            if cells[0] == 'e' and cells[1].isdigit() and cells[3].isdigit():
                                self.board[x][y] = self.board[x][y][1]
                                something_changed = 1
                            elif cells[2] == 'e' and cells[1].isdigit() and cells[4].isdigit():
                                self.board[x][y] = self.board[x][y][1]
                                something_changed = 1
                            elif cells[5] == 'e' and cells[3].isdigit() and cells[6].isdigit():
                                self.board[x][y] = self.board[x][y][1]
                                something_changed = 1
                            elif cells[7] == 'e' and cells[4].isdigit() and cells[6].isdigit():
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
                if self.board[x][y][0] in ["hb","fb"]:
                    self.board[x][y] = self.board[x][y][1]


    def update(self,x,y,op='o'):
        '''
        def:
            reveals or flags the (x,y) cell
            updates the rest of the board if a cell was revealed
        input:
            op = default no-op, if 'flag' flags cell
            x = x cord
            y = y cord
        '''
        if self.board[y][x].isdigit() or self.board[y][x] == 'e':
            raise ValueError("that cell is already revealed")
        elif op == 'f':
            self.board[y][x]= 'f'+self.board[y][x][1]
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
            csv_file.writerow([self.width,self.height])
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

        # getting width and height
        self.width = int(data[0][0])
        self.height = int(data[0][1])

        # copying the rest
        self.board = []
        for i in range(1,len(data)):
            self.board.append(data[i])
