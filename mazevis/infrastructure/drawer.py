"""Handles graphical interactions for the mazevis application."""
import tkinter
from mazevis.infrastructure import grid
from mazevis.constants import graphical_constants as g_const


class MazeDrawer(tkinter.Frame):
    """Contains information and functions
    to draw two-dimensional cell grids.
    """

    def __init__(self, maze_grid: grid.MazeGrid, offset_x, offset_y,
                 px_per_cell=g_const.CELL_SIZE):
        super().__init__()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.px_per_cell = px_per_cell
        self.px_per_line = 2
        self.maze_grid = maze_grid
        self.items = {}
        # graphical elements
        canvas_width = (self.offset_x * 2 +
                        self.px_per_cell * self.maze_grid.get_cell_width())
        canvas_height = (self.offset_y * 2 +
                         self.px_per_cell * self.maze_grid.get_wall_height())
        self.canvas = tkinter.Canvas(self, width=canvas_width,
                                     height=canvas_height)
        self.canvas.pack()
        self.container = self.generate_container()

    def draw_grid(self):
        """Draws the entire cell grid including a border."""
        # print border
        grid_width = self.px_per_cell * self.maze_grid.get_cell_width()
        grid_height = self.px_per_cell * self.maze_grid.get_cell_height()
        self.canvas.create_rectangle(self.offset_x,
                                     self.offset_y,
                                     self.offset_x + grid_width,
                                     self.offset_y + grid_height)
        # draw walls
        for x in range(self.maze_grid.get_wall_width()):
            for y in range(self.maze_grid.get_wall_height()):
                node = self.maze_grid.get_wall_at(x, y)
                if node is True:
                    if x % 2 == 1:
                        self.draw_vertical_wall((x, y))
                    if y % 2 == 1:
                        self.draw_horizontal_wall((x, y))
        # draw special cells
        for x in range(self.maze_grid.get_cell_width()):
            for y in range(self.maze_grid.get_cell_height()):
                cl = self.maze_grid.get_cell_at(x, y)
                if cl.is_base():
                    self.draw_base_at(x, y)
                if cl.has_item():
                    self.draw_item_at((x, y))

    def draw_vertical_wall(self, p1):
        """Draws a vertical cell wall at the specified wall-coordinates."""
        # p1 from grid.walls coordinates
        x1_wall, y1_wall = p1
        x1_px = self.offset_x + self.px_per_cell * ((x1_wall + 1) / 2)
        x2_px = x1_px
        y1_px = self.offset_y + self.px_per_cell * (y1_wall / 2)
        y2_px = y1_px + self.px_per_cell
        shape = self.canvas.create_line(x1_px, y1_px, x2_px, y2_px)
        self.container[x1_wall][y1_wall] = shape

    def draw_horizontal_wall(self, p1):
        """Draws a horizontal cell wall at the specified wall-coordinates."""
        # p1 from grid.walls coordinates
        x1_wall, y1_wall = p1
        x1_px = self.offset_x + self.px_per_cell * (x1_wall / 2)
        x2_px = x1_px + self.px_per_cell
        y1_px = self.offset_y + self.px_per_cell * ((y1_wall + 1) / 2)
        y2_px = y1_px
        # draw and memorize
        shape = self.canvas.create_line(x1_px, y1_px, x2_px, y2_px)
        self.container[x1_wall][y1_wall] = shape

    def undraw_wall(self, p1):
        """Deletes a cell wall a the specified wall-coordinates"""
        x1_wall, y1_wall = p1
        wall = self.container[x1_wall][y1_wall]
        self.canvas.delete(wall)

    def draw_base_at(self, x, y):
        """Draws a base representation at the specified cell-coordinates."""
        x1_px, y1_px = self.get_p1cell_px((x, y))
        x2_px, y2_px = self.get_p2cell_px((x, y))
        self.canvas.create_oval(x1_px, y1_px, x2_px, y2_px,
                                outline=g_const.BASE_FG,
                                fill=g_const.BASE_BG)

    def draw_item_at(self, p_cell):
        p1_px = self.get_p1cell_px(p_cell)
        p2_px = self.get_p2cell_px(p_cell)
        padding = int(self.px_per_cell / 4)
        x1, y1 = p1_px
        x2, y2 = p2_px
        x1 += padding
        y1 += padding
        x2 -= padding
        y2 -= padding
        shape = self.canvas.create_rectangle(x1, y1, x2, y2,
                                             outline=g_const.ITEM_FG,
                                             fill=g_const.ITEM_BG)
        self.items[p_cell] = shape

    def get_p1cell_px(self, p_cell):
        x_cell, y_cell = p_cell
        x_px = self.offset_x + self.px_per_cell * x_cell
        y_px = self.offset_y + self.px_per_cell * y_cell
        return x_px, y_px

    def get_p2cell_px(self, p_cell):
        x_cell, y_cell = p_cell
        x_px = self.offset_x + self.px_per_cell * (x_cell + 1)
        y_px = self.offset_y + self.px_per_cell * (y_cell + 1)
        return x_px, y_px

    def generate_container(self):
        """Generates an empty 2-dimensional grid the sized for containing
        walls according to self.mazegrid.
        """
        return [[None for _ in range(self.maze_grid.get_wall_height())]
                for _ in range(self.maze_grid.get_wall_width())]
