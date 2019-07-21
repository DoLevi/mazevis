"""Handles cell class properties for the mazevis application."""


class Cell:
    """Contains information and functions for handling single cells."""

    def __init__(self):
        self.visited = False
        self.base = False
        self.item_points = None

    def is_visited(self):
        """Returns 'True' if the cell object has been visited,
        'False' otherwise. [Used by maze generation algorithm.]
        """
        return self.visited

    def mark_visited(self):
        """Marks the cell object as visited.
        [Used by maze generation algorithm.]
        """
        self.visited = True

    def is_base(self):
        return self.base

    def mark_base(self):
        self.base = True

    def has_item(self):
        return bool(self.item_points)

    def assign_item(self, points):
        self.item_points = points
