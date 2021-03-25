from node import Node
from gui import Gui
import pygame


def depthFirst(gui:Gui, start:Node, end:Node) -> bool:
    """Runs Depth-First Search Algorithm

    This algorithm explores as far as possible along each branch of a tree (or graph) before backtracking.

    Reference = [https://en.wikipedia.org/wiki/Depth-first_search]

    Parameters
    ----------
    nodes : list
        A list of nodes present in the grid
    start : Node
        The starting point
    end : Node
        The ending point

    Returns
    -------
    bool
        True if the ending node was reached, else False
    """
    def buildReversePath(came_from:dict, current:Node):
        while current in came_from:
            current = came_from[current]
            current.setState("path")
            gui.updateContents()

    came_from = {}
    open_set = [start] # The LIFO data structure for exploring as far as possible along each branch
    visited = []

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui.close()

        current = open_set.pop(-1)
        visited.append(current)

        if current == end:
            buildReversePath(came_from, end)
            end.setState("end point")
            start.setState("start point")
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                open_set.append(neighbor)
                neighbor.setState("watch")
                gui.updateContents()

        if current != start:
            current.setState("visited")
            gui.updateContents()

    return False