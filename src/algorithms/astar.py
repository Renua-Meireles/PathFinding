from queue import PriorityQueue
from node import Node
from gui import Gui
import pygame


def aStar(gui:Gui, start:Node, end:Node) -> bool:
    """Runs A* algorithm

    One important aspect of A* is f = g + h
    Where:
        f is the total cost of the node.
        g is the distance between the current node and the start node.
        h is the heuristic - estimated distance from the current node to the end node.

    This algorithm expoits the node with the lowest f and its neighbors.

    Reference = [https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2]
    Code adapted from = [https://morioh.com/p/cf0c6b11c848?f=5c21fb01c16e2556b555ab32]

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
    def h(node1:Node, node2:Node):
        return abs(node1.row - node2.row) + abs(node1.col - node2.col)

    def buildReversePath(came_from:dict, current:Node):
        while current in came_from:
            current = came_from[current]
            current.setState("path")
            gui.updateContents()
            
    g = 0
    open_set = PriorityQueue()  # tip: A structure that it's always sorted (first f then h...). Method get() gets the first element (lowest f).
    open_set.put((0, g, start))
    came_from = {}
    g_score = {node: float("inf") for node in gui.grid}
    g_score[start] = 0
    f_score = {node: float("inf") for node in gui.grid}
    f_score[start] = h(start, end)

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui.close()

        *_, current = open_set.get()
        open_set_hash.remove(current)

        if current == end:
            buildReversePath(came_from, end)
            end.setState("end point")
            start.setState("start point")
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor, end)
                if neighbor not in open_set_hash:
                    g += 1
                    open_set.put((f_score[neighbor], g, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.setState("watch")
                    gui.updateContents()

        if current != start:
            current.setState("visited")
            gui.updateContents()

    return False