"""Handles cell class properties for the mazevis application."""


class Cell:
    """Contains information and functions for handling single cells."""

    def __init__(self):
        self.visited = False

    def is_visited(self):
        """Returns 'True' if the cell object has been visited,
        'False' otherwise.
        """
        return self.visited

    def mark_visited(self):
        """Marks the cell object as visited."""
        self.visited = True
