"""Driver module for execution for the mazevis application."""
from mazevis.infrastructure import starter

UPDATE_RATE = None

CELL_COLUMNS = 28
CELL_ROWS = 15
BASE_SIZE = 3


def compute_lbase(rows, block_size):
    """Computes and returns vertically centered coordinates
    for the left base.
    """
    base_offset_h = int((rows - block_size) / 2)
    lbase_p1 = (0, base_offset_h)
    lbase_p2 = (block_size, base_offset_h + block_size)
    return lbase_p1, lbase_p2


def compute_rbase(rows, cols, block_size):
    """Computes and returns vertically centered coordinates
    for the right base.
    """
    base_offset_h = int((rows - block_size) / 2)
    rbase_p1 = (cols - block_size, base_offset_h)
    rbase_p2 = (cols, base_offset_h + block_size)
    return rbase_p1, rbase_p2


if __name__ == '__main__':
    LBASE = compute_lbase(CELL_ROWS, BASE_SIZE)
    RBASE = compute_rbase(CELL_ROWS, CELL_COLUMNS, BASE_SIZE)
    VIS = starter.MazeVisualizer(CELL_COLUMNS, CELL_ROWS, UPDATE_RATE,
                                 LBASE, RBASE)
    VIS.updater()
    VIS.do_mainloop()
