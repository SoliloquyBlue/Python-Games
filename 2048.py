"""
Clone of 2048 game.
"""
import random
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = []
    for tile in line:
        if tile:
            result.append(tile)
    index = 0

    while index < len(result) - 1:
        item1 = result[index]
        item2 = result[index + 1]

        if item1 == item2:
        #Do comparison here and assign new values to lst
            result[index] = item1 + item2
            result[index + 1] = 0
            index += 2
        else:
            index += 1
            
    while len(result) < len(line):
        result.append(0)
    result = compress(result)

    return result

def compress(line):
    """
    Helper function that removes zeros on the left and adds
    them on the right.
    """
    result = []
    for tile in line:
        if tile > 0:
            result.append(tile)
    while len(result) < len(line):
        result.append(0)
    return result

    
class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._changed = False
        
        # indices for directions
        self._up_indices = [('','' )] * self._grid_width
        self._down_indices = [('','' )] * self._grid_width
        self._left_indices = [('','')] * self._grid_height
        self._right_indices =  [('','')] * self._grid_height
        
        for dummy_idx in range(self._grid_width):
            self._up_indices[dummy_idx] = (0, dummy_idx)
            self._down_indices[dummy_idx] = (self._grid_height-1, dummy_idx)
        for dummy_jax in range(self._grid_height):
            self._left_indices[dummy_jax] = (dummy_jax, 0)
            self._right_indices[dummy_jax] = (dummy_jax, self._grid_width-1)
            
        self._indices = {UP: self._up_indices,
           DOWN: self._down_indices,
           LEFT: self._left_indices,
           RIGHT: self._right_indices}
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = []
        self._cells = [[0 for dummy_col in range(self._grid_width)]
           for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # uses built-in str() function, thank you Python
        #return str(self._cells)
        return str([x for x in self._cells]).replace("],", "]\n")

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def find_empty(self):
        """
        Creates a list of empty tiles to place a new tile in.
        """
        self._empty_list = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._cells[row][col] == 0:
                    self._empty_list.append([row, col])
        
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        before = self.__str__()
        merged_cells = []
        if direction is UP or direction is DOWN:
            num_steps = self._grid_height
        else:
            num_steps = self._grid_width
            
        for dummy_each in self._indices[direction]:
            temp = []
            for dummy_step in range(num_steps):
                row = dummy_each[0] + OFFSETS[direction][0] * dummy_step
                col = dummy_each[1] + OFFSETS[direction][1] * dummy_step
                temp.append(self._cells[row][col])
                merged_line = merge(temp)
                merged_cells.append(merged_line)
            for dummy_step in range(num_steps):
                row = dummy_each[0] + OFFSETS[direction][0] * dummy_step
                col = dummy_each[1] + OFFSETS[direction][1] * dummy_step
                self._cells[row][col] = merged_line.pop(0)
        if self.__str__() != before:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        self.find_empty()
        num_empty = len(self._empty_list)
        if num_empty > 0:
            random_tile = random.randrange(num_empty)
            random_number = random.randint(0,99)
            if random_number <= 89:
                value = 2
            else:
                value = 4
            random_tile = self._empty_list[random_tile]
#            print random_tile, value
            self.set_tile(random_tile[0], random_tile[1], value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._cells[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
#TwentyFortyEight(4, 4)
