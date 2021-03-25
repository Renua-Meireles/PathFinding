import pygame
from node import Node, Square, Hexagon
import colors

class Gui(object):
    """A class that handles the user interface
    """

    def __init__(self, width = 1000, height = 700, padding = (0, 0, 0, 0), gap = 1, node_size = 25, fps = 120):
        """Class constructor

        Parameters
        ----------
        width : int, optional
            The width of the window, by default 1000
        height : int, optional
            The height of the window, by default 700
        padding : tuple, optional
            The left, right, bottom and top respectively paddings of the window, by default (0, 0, 0, 0)
        gap : int, optional
            The gap between the nodes, by default 1
        node_size : int, optional
            The size of the node, by default 25
        fps : int, optional
            The amount of frames per second, by default 120
        """
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Gui')
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.padding = padding

        self.grid = []
        self.gap = gap
        self.window.fill(colors.GREY)
        Node.size = node_size
        self.drawNodes()
        self.drawBorders()
        

    def drawNodes(self) -> None:
        """Draws and positionates all nodes at the window
        """
        pad_r, pad_l, pad_bot, pad_top = self.padding

        # finding how many nodes are possible to place
        partition = Node.size + self.gap

        h_available_space = self.window.get_width() - pad_r - pad_l
        v_available_space = self.window.get_height() - pad_bot - pad_top
        self.horizontal_nodes = h_available_space // partition
        self.vertical_nodes = v_available_space // partition
        
        # Finding the vertical and horizontal starting points that centers the nodes
        x0 = (self.window.get_width() - (self.horizontal_nodes * partition)) // 2
        y0 = (self.window.get_height() - (self.vertical_nodes * partition)) // 2

        # Generating the nodes
        self.grid = [
            Square(row, col, partition, x0, y0, self.window)
            for row in range(self.vertical_nodes) for col in range(self.horizontal_nodes)
        ]
    
    def drawBorders(self):
        """Draws the borders of the grid
        """
        width = 1
        color = colors.BLACK
        x0, y0 = self.grid[0].x0 - width, self.grid[0].y0 - width
        h_end = self.grid[-1].y0 + Node.size
        v_end = self.grid[-1].x0 + Node.size
        
        points = [(x0, y0), (x0, h_end), (v_end, h_end), (v_end, y0)]
        pygame.draw.lines( self.window, color, closed=True, points=points , width=width)
        

    def setNodeColor(self, mouse_xy:tuple, start_node:Node, end_node:Node) -> tuple:
        """Seeks for the node that the mouse clicked on and changes its color

        Parameters
        ----------
        mouse_xy : tuple
            The mouse vertical and horizontal pixel values
        start_node : Node
            The node that it's already setted as the start node
        end_node : Node
            The node that it's already setted as the end node

        Returns
        -------
        tuple
            The starting and ending nodes
        """
        for node in self.grid:
            if node.isCoordinateIn(*mouse_xy):
                if not start_node:
                    node.setState("start point")
                    start_node = node
                elif not end_node and node != start_node:
                    node.setState("end point")
                    end_node = node
                elif node != end_node and node != start_node:
                    node.setState("wall")  
                break  

        return start_node, end_node
                
    def resetNodeColor(self, mouse_xy:tuple, start_node:Node, end_node:Node) -> tuple:
        """Seeks for the node that the mouse clicked on and resets its color

        Parameters
        ----------
        mouse_xy : tuple
            The mouse vertical and horizontal pixel values
        start_node : Node
            The node that it's already setted as the start node
        end_node : Node
            The node that it's already setted as the end node

        Returns
        -------
        tuple
            The starting and ending nodes
        """
        for node in self.grid:
            if node.isCoordinateIn(*mouse_xy):
                node.setState("empty")
                if node == start_node:
                    start_node = None
                if node == end_node:
                    end_node = None
                break
        return start_node, end_node
    

    def updateNodeNeighbors(self) -> None:
        """Updates all the neighbors of each node
        """
        for node in self.grid:
            node.updateNeighbors(self.grid, self.horizontal_nodes, self.vertical_nodes)


    def updateContents(self) -> None:
        """Updates the window content
        """
        self.clock.tick(self.fps)
        pygame.display.flip()
    
    def reset(self, exeptions=[]) -> None:
        """Resets the contents of the window
        """
        nodes = filter(lambda node: node.state not in exeptions, self.grid)
        for node in nodes:
            node.setState("empty")

    def close(self) -> None:
        """Closes the pygame window
        """
        pygame.quit()
        exit(1)