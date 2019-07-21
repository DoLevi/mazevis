"""Driver module for execution for the mazevis application."""
import tkinter
from mazevis.infrastructure import drawer
from mazevis.infrastructure import grid


class MazeVisualizer:
    """Class containing functions to format and initialize the mazevis
    application."""

    def __init__(self, cell_columns, cell_rows, update_rate,
                 lbase_coords, rbase_coords):
        self.root = MazeVisualizer.generate_root()
        root_frame = tkinter.Frame(self.root)
        root_frame.pack()
        # initialize grid
        self.maze_grid = grid.MazeGrid(cell_columns, cell_rows, 0, 0,
                                       lbase_coords, rbase_coords)
        self.update_rate = update_rate
        if not self.update_rate:
            print("Grid will be created initially.")
            self.maze_grid.generate_maze()
            self.maze_grid.spawn_bases()
            self.maze_grid.spawn_items()
            # initialize drawer
        self.maze_drawer = drawer.MazeDrawer(self.maze_grid, 20, 40)
        self.maze_drawer.pack(side=tkinter.TOP)
        self.maze_drawer.draw_grid()

    @staticmethod
    def generate_root():
        """Generates a TK instance half the size of the screen."""
        root = tkinter.Tk()
        center_x = root.winfo_screenwidth() / 2
        center_y = root.winfo_screenheight() / 2
        window_x = center_x / 2
        window_y = center_y / 2
        coords = "{}x{}+{}+{}".format(int(center_x), int(center_y),
                                      int(window_x), int(window_y))
        root.geometry(coords)
        return root

    def updater(self):
        """Updates the application state (logical + graphical)."""
        removed_wall = self.maze_grid.next_step()
        if removed_wall is None:
            print("Finished")
        else:
            self.maze_drawer.undraw_wall(removed_wall)
            self.root.after(self.update_rate, self.updater)

    def do_mainloop(self):
        self.root.mainloop()
