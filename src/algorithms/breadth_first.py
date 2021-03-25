from node import Node
from gui import Gui
import pygame


def breadthFirstSearch(gui:Gui, start:Node, end:Node) -> bool:
    """Runs A* algorithm

    This algorithm explores all of the neighbor nodes at the present
    depth prior to moving on to the nodes at the next depth level.

    Reference = [https://en.wikipedia.org/wiki/Breadth-first_search]

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
    open_set = [start] # The FIFO data structure for exploring all of the neighbor nodes as soon as they shows up
    visited = []

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui.close()

        current = open_set.pop(0)
        visited.append(current)

        if current == end:
            buildReversePath(came_from, end)
            end.setState("end point")
            start.setState("start point")
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and neighbor.state != "watch":
                open_set.append(neighbor)
                came_from[neighbor] = current
                neighbor.setState("watch")
                gui.updateContents()

        if current != start:
            current.setState("visited")
            gui.updateContents()

    return False