"""Driver module for execution for the mazevis application."""
import tkinter
from mazevis.infrastructure import drawer
from mazevis.infrastructure import grid

UPDATE_RATE = 10

CELL_COLUMNS = 28
CELL_ROWS = 15


class MazeVisualizer:
    """Class containing functions to format, initialize and launch mazevis
    application."""

    def __init__(self):
        self.root = MazeVisualizer.generate_root()
        root_frame = tkinter.Frame(self.root)
        root_frame.pack()
        self.maze_grid = grid.MazeGrid(CELL_COLUMNS, CELL_ROWS, 0, 0)
        self.maze_drawer = drawer.MazeDrawer(self.maze_grid, 20, 40)
        self.maze_drawer.pack(side=tkinter.TOP)
        self.maze_drawer.draw_grid()

    @staticmethod
    def generate_root():
        """Generates a TK instance half the screen size."""
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
            self.root.after(UPDATE_RATE, self.updater)


if __name__ == '__main__':
    VIS = MazeVisualizer()
    VIS.updater()
    VIS.root.mainloop()
