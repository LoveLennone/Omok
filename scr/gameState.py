from tkinter import Y
from StonePiece import StonePiece

board_size = 15
MATRIX = [[0 for x in range(board_size)] for y in range(board_size)]

# for i in range(board_size):
#     for j in range(board_size):
#         MATRIX[i][j] = "empty"

bC = StonePiece(1, 0, 'black')
wC = StonePiece(1, 0, 'white')
#MATRIX[0][0] = bC
#MATRIX[2][3] = wC

class GameState:
    def __init__(self, **args):
        self.highlightSwitch = 0
        self.dimension = args['dimension']
        self.matrix = MATRIX #Grid(self.dimension, self.dimension)
        self.player_turn = 0 # Even : black / Odd : white
        self.win_history = [0, 0, 0] # black, white, draw

    def __str__(self):
        width, height = self.dimension, self.dimension
        map = Grid(width, height)
        for row in range(width):
            for col in range(height):
                if self.getColor(row, col) == 'black':
                    map[col][row] = 'x'
                elif self.getColor(row, col) == 'white':
                    map[col][row] = 'o'
                else:
                    map[col][row] = 'F'
        return str(map) #+ ("\nScore: %d\n" % self.score)

    def flip_highlight_switch(self, value):
        self.highlightSwitch = value

    def get_highlight_switch(self):
        return self.highlightSwitch

    def is_invalid(self, x, y):
        return (x < 0 or x >= board_size or y < 0 or y >= board_size)

    def is_gameOver(self, x, y, stone):

        '''
        for i in range(h):
            for j in range(h):
                TODO: "GO through matrix and determine if win condition and player turn"
                if MATRIX[i][j] something
        '''

        if self.player_turn >= self.dimension * self.dimension: # Draw
            self.winCount('draw')
            return True

        ori_x, ori_y = x, y
        n_dx = [0, 0, 1, -1, -1, 1, -1, 1]
        n_dy = [-1, 1, -1, 1, 0, 0, -1, 1]
        #print(stone, self.matrix[x][y].get_color())

        for direct in range(0, len(n_dy), 2):
            cnt = 1
            for next in range(direct, direct + 2):
                dx, dy = n_dx[next], n_dy[next]
                x, y = ori_x, ori_y
                
                while True:
                    x, y = x + dx, y + dy
                    #print(stone, x, y, dx, dy, cnt)
                    
                    if self.checkLocation(x, y, self.dimension) == False or self.matrix[x][y] == 0:
                        break
                    elif self.getColor(x, y) == stone:
                        cnt += 1
                    else:
                        break
                    
            if cnt >= 5:
                self.winCount(stone)
                #print("player " + stone + " wins!!")
                return True
        return False

    def winCount(self, color):
        if color == 'black':
            self.win_history[0] += 1 
        if color == 'white':
            self.win_history[1] += 1
        if color == 'draw':
            self.win_history[2] += 1

    def checkLocation(self, row, col, dimension):
        if col < 0 or col >= dimension or row < 0 or row >= dimension:
            #print("Placing error!", col, row)
            return False
        return True

    def updatePlayerTurn(self, row, col):
        if self.matrix[row][col] == 0:
            if self.player_turn % 2 == 0:
                self.matrix[row][col] = StonePiece(row, col, 'black')
            elif self.player_turn % 2 == 1:
                self.matrix[row][col] = StonePiece(row, col, 'white')
            self.player_turn += 1

    def getPlayerTurn(self):
        return self.player_turn

    def getColor(self, row, col):
        if self.matrix[row][col] == 0:
            return None
        return self.matrix[row][col].get_color()

    def deepCopy(self):
        state = GameState(dimension=self.dimension)
        state.matrix = [x[:] for x in self.matrix]
        state.player_turn = self.player_turn
        return state

    def reset(self):
        self.highlightSwitch = 0
        self.player_turn = 0
        self.matrix = [[0 for x in range(board_size)] for y in range(board_size)]
        #self.win_history = [0, 0, 0]
        #print(self.matrix)

    def generateSuccessor(self, action):
        succss = self.deepCopy()
        x, y = action
        succss.updatePlayerTurn(x, y)
        return succss

    def getCenter(self):
        return (int(self.dimension/2), int(self.dimension/2))


class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Omok map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a Omok board.
    """

    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]:
            raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)]
               for y in range(self.height)]
        # out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other == None:
            return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def asList(self, key=True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    list.append((x, y))
        return list

    def packBits(self):
        """
        Returns an efficient int list representation

        (width, height, bitPackedInts...)
        """
        bits = [self.width, self.height]
        currentInt = 0
        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cellIndexToPosition(i)
            if self[x][y]:
                currentInt += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(currentInt)
                currentInt = 0
        bits.append(currentInt)
        return tuple(bits)

    def _cellIndexToPosition(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def _unpackBits(self, bits):
        """
        Fills in data from a bit-level representation
        """
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height:
                    break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0:
            raise ValueError("must be a positive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools




