"""Handles logical cell grid interactions for the mazevis application."""
import random
from mazevis.infrastructure import cell


class MazeGrid:
    """Contains information and functions for handling
    a grid of cell objects.
    """

    def __init__(self, width, height, initial_x, initial_y,
                 lbase_coords, rbase_coords):
        self.width = width
        self.height = height
        self.walls = self.generate_wall_grid()
        self.grid = self.generate_cell_grid()
        self.stack = []
        if self.are_in_boundaries(initial_x, initial_y):
            self.current_coordinates = (initial_x, initial_y)
            self.mark_current_as_visited()
        else:
            error = ("Coordinates ({}|{}) are out-of-bounds ({}|{})"
                     .format(initial_x, initial_y, self.width - 1,
                             self.height - 1))
            raise ValueError(error)
        self.lbase_p1, self.lbase_p2 = lbase_coords
        self.rbase_p1, self.rbase_p2 = rbase_coords

    # public-ey functions

    def get_cell_width(self):
        """Returns the width of the grid in number of cells objects."""
        return self.width

    def get_cell_height(self):
        """Returns the height of the grid in number of cells objects."""
        return self.height

    def get_wall_width(self):
        """Returns the width of the grid in number of wall objects."""
        return 2 * self.width - 1

    def get_wall_height(self):
        """Returns the height of the grid in number of wall objects."""
        return 2 * self.height - 1

    def get_wall_at(self, x, y):
        """Returns the wall object at the specified wall-coordinates."""
        return self.walls[x][y]

    def next_step(self):
        """Advances the grid one step further
        in the maze generation algorithm execution.
        """
        if self.current_coordinates is None:
            error = "Variable 'current_coordinates' has not been set"
            raise UnboundLocalError(error)
        next_current = self.get_random_unvisited_neighbour()
        if next_current is not None:
            self.stack.append(self.current_coordinates)
            coords = self.open_wall(self.current_coordinates, next_current)
            self.current_coordinates = next_current
            self.mark_current_as_visited()
            return coords
        if len(self.stack) > 0:
            self.current_coordinates = self.stack.pop()
            return self.next_step()
        return None

    def generate_maze(self):
        while self.next_step() is not None:
            pass
        lbase_x1, lbase_y1 = self.lbase_p1
        lbase_x2, lbase_y2 = self.lbase_p2
        # remove walls in left base
        for col_idx in range(lbase_x1, lbase_x2):
            for row_idx in range(lbase_y1, lbase_y2):
                cell_p1 = col_idx, row_idx
                right_wall_p2 = col_idx + 1, row_idx
                lower_wall_p2 = col_idx, row_idx + 1
                self.open_wall(cell_p1, right_wall_p2)
                self.open_wall(cell_p1, lower_wall_p2)
        rbase_x1, rbase_y1 = self.rbase_p1
        rbase_x2, rbase_y2 = self.rbase_p2
        # remove walls in right base
        for col_idx in range(rbase_x1, rbase_x2):
            for row_idx in range(rbase_y1, rbase_y2):
                cell_p1 = col_idx, row_idx
                right_wall_p2 = col_idx + 1, row_idx
                lower_wall_p2 = col_idx, row_idx + 1
                self.open_wall(cell_p1, right_wall_p2)
                self.open_wall(cell_p1, lower_wall_p2)

    # private-y functions

    @staticmethod
    def are_adjacent(p1, p2):
        """Checks whether cell-coordinates are adjacent
        and returns the result as a bool value.
        """
        x1, y1 = p1
        x2, y2 = p2
        if abs(abs(x2 - x1) - abs(y2 - y1)) == 1:
            return True
        return False

    def generate_cell_grid(self):
        """Generates an empty cell grid
        according to self.height and self.width.
        """
        return [[cell.Cell() for _ in range(self.height)]
                for _ in range(self.width)]

    def generate_wall_grid(self):
        """Generates a wall grid according to self.height and self.width."""
        full_grid = [[]]
        for x in range(2 * self.width):
            full_grid.append([])
            for y in range(2 * self.height):
                full_grid[x].append(None)
                # only consider walls, not cells or corners
                full_grid[x][y] = True if x % 2 != y % 2 else None
        return full_grid

    def are_in_boundaries(self, x, y):
        """Checks whether the specified cell-coordinates are within the grid
        and returns the result as a bool value.
        """
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return True
        return False

    def check_valid_adjacent_cells(self, p1, p2):
        """Checks whether cell-coordinates belong to adjacent cells
        and whether they are within the grids boundaries.
        """
        x1, y1 = p1
        x2, y2 = p2
        if not MazeGrid.are_adjacent(p1, p2):
            error = ("Cells ({}|{}) and ({}|{}) are not adjacent"
                     .format(x1, y1, x2, y2))
            raise ValueError(error)
        if (not (self.are_in_boundaries(x1, y1) and
                 self.are_in_boundaries(x2, y2))):
            error = ("Cells are out-of-bounds ({} | {}) and ({} | {})"
                     .format(x1, y1, x2, y2))
            raise ValueError(error)

    def get_random_unvisited_neighbour(self):
        """Returns the cell-coordinates of a random neighbouring cell."""
        x, y = self.current_coordinates
        neighbour_coordinates = []
        if (y - 1 >= 0) and (not self.grid[x][y - 1].is_visited()):
            # upper cell
            neighbour_coordinates.append((x, y - 1))
        if (x + 1 < self.width) and (not self.grid[x + 1][y].is_visited()):
            # right cell
            neighbour_coordinates.append((x + 1, y))
        if (y + 1 < self.height) and (not self.grid[x][y + 1].is_visited()):
            # lower cell
            neighbour_coordinates.append((x, y + 1))
        if (x - 1 >= 0) and (not self.grid[x - 1][y].is_visited()):
            # left cell
            neighbour_coordinates.append((x - 1, y))
        # choose element
        if not neighbour_coordinates:
            return None
        # [print("{}|{}".format(cl[0], cl[1])) for cl in neighbour_coordinates]
        return random.choice(neighbour_coordinates)

    def mark_current_as_visited(self):
        """Marks the cell at self.current_cell as visited."""
        x, y = self.current_coordinates
        self.grid[x][y].mark_visited()

    def open_wall(self, p1, p2):
        """Opens the wall between the cells at the specified
        cell-coordinates.
        """
        self.check_valid_adjacent_cells(p1, p2)
        x1, y1 = p1
        x2, y2 = p2
        x_of_wall = x1 + x2
        y_of_wall = y1 + y2
        self.walls[x_of_wall][y_of_wall] = False
        return x_of_wall, y_of_wall
