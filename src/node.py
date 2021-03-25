import math
import pygame
import colors

class Node(object):
    size = 0
    max_neighbors = 0
    def __init__(self, row:int, col:int, part:int, pad_x:int, pad_y:int, window: pygame.Surface) -> None:
        """A class that represents a unique node in the grid of the Window

        Parameters
        ----------
        row : int
            The row index of the node
        col : int
            The columns index of the node
        part : int
            The space occupied by a node and a gap, useful for pixel coordinate definition
        pad_x : int
            The initial horizontal pixel position
        pad_y : int
            The initial vertical pixel position
        window : pygame.Surface
            The window where the node will be drawn
        """
        
        self.row = row
        self.col = col
        self.x0 = (col * part) + pad_x
        self.y0 = (row * part) + pad_y
        self.window = window
        self.neighbors = []
        self.state_color_map = {
            "empty": colors.WHITE,
            "wall": colors.BLACK,
            "start point": colors.GREEN,
            "end point": colors.RED,
            "path": colors.TURQUOISE,
            "visited": colors.ORANGE,
            "watch": colors.PURPLE
        }
    

    def setState(self, state:str) -> None:
        """Sets the state of the node

        Parameters
        ----------
        state : str
            The state to be received
        """
        if not state in self.state_color_map.keys():
            raise AttributeError(
                f'The state "{state}" has not been defined in "Node.state_color_map".\n' + 
                f'States currently defined: {self.state_color_map.keys()}'
            )

        self.state = state
        self.draw()

    def getColor(self) -> tuple:
        """Gets the color based on the current state of the node

        Returns
        -------
        tuple
            The RGB color
        """
        return self.state_color_map[self.state]


    def draw(self) -> None:
        """Draws the node on the window
        """
        raise NotImplementedError

    def isCoordinateIn(self) -> bool:
        """Indicates whether a given pixel coordinate is part of the node
        """
        raise NotImplementedError

    def updateNeighbors() -> None:
        """Seeks for the adjacent nodes
        """
        raise NotImplementedError


    
    def __eq__(self, other: object) -> bool:
        if not other:
            return False
        return (self.row == other.row) and (self.col == other.col)

    def __repr__(self) -> str:
        return f'Node({self.row}, {self.col})'
    
    def __hash__(self) -> int:
        # Ajusting the class to be hashable based on its representation (__repr__)
        # This allows for example using nodes instances as keys in dictionaries.
        return hash(str(self))

    __str__ = __repr__



class Square(Node):
    def __init__(self, row:int, col:int, part:int, pad_x:int, pad_y:int, window: pygame.Surface) -> None:
        super().__init__(row, col, part, pad_x, pad_y, window)
        self.form =  pygame.Rect(self.x0, self.y0, self.size, self.size)
        self.setState("empty")
        self.max_neighbors = 4
        

    def draw(self) -> None:
        """Draws the node on the window
        """

        color = self.getColor()
        pygame.draw.rect(self.window, color, self.form)
            

    def updateNeighbors(self, grid:list, h_nodes:int, v_nodes:int) -> None:
        """Seeks for the adjacent nodes

        Parameters
        ----------
        grid : list
            The list containing all nodes of the grid
        h_nodes : int
            Amount of horizontal nodes
        v_nodes : int
            Amount of vertical nodes
        """

        idx = (self.row * h_nodes) + self.col
        cond_idx = [
            (0 < self.col, idx-1),       (self.col < h_nodes-1, idx+1), # HORIZONTAL ADJACENT NODES
            (0 < self.row, idx-h_nodes), (self.row < v_nodes-1, idx+h_nodes) # VERTICAL ADJACENT NODES
        ]
        self.neighbors = [grid[i] for condition, i in cond_idx if condition and grid[i].state!="wall"]
        

    def isCoordinateIn(self, x:int, y:int) -> bool:
        """Indicates whether a given pixel coordinate is part of the node

        Parameters
        ----------
        x : int
            The horizontal pixel value
        y : int
            The vertical pixel value

        Returns
        -------
        bool
            True, if received coordinate it's part of the node
        """
        # x_end, y_end = self.x0 + Node.size, self.y0 + Node.size
        # return (self.x0 <= x <= x_end) and (self.y0 <= y <= y_end)
        return self.form.collidepoint((x, y))





class Hexagon(Node):
    def __init__(self, row:int, col:int, part:int, pad_x:int, pad_y:int, window: pygame.Surface) -> None:
        super().__init__(row, col, part, pad_x, pad_y, window)
        self.max_neighbors = 6
        
        self.y0 += self.size/2 if col % 2 != 0 else 0

        r = self.size / 2
        x = self.x0 + r
        y = self.y0 + r
        self.form = [
            (
                x + r * math.cos(2 * math.pi * i / 6), 
                y + r * math.sin(2 * math.pi * i / 6)
            )
            for i in range(6)
        ]
        self.setState("empty")
        

    def draw(self) -> None:
        """Draws the node on the window
        """

        color = self.getColor()
        pygame.draw.polygon(self.window, color, self.form)
            

    def updateNeighbors(self, grid:list, h_nodes:int, v_nodes:int) -> None:
        """Seeks for the adjacent nodes

        Parameters
        ----------
        grid : list
            The list containing all nodes of the grid
        h_nodes : int
            Amount of horizontal nodes
        v_nodes : int
            Amount of vertical nodes
        """

        idx = (self.row * h_nodes) + self.col
        cond_idx = [
            (0 < self.col, idx-1),       (self.col < h_nodes-1, idx+1), # HORIZONTAL ADJACENT NODES = UPPER DIOGONAL NODES
            (0 < self.row, idx-h_nodes), (self.row < v_nodes-1, idx+h_nodes), # VERTICAL ADJACENT NODES = UPPER NODE
            (self.row < v_nodes-1, idx-h_nodes-1), (self.row < v_nodes-1, idx+h_nodes+1) # BOTTOM -1/+1 ADJACENT NODES = LOWER DIOGONAL NODES
        ]
        self.neighbors = [grid[i] for condition, i in cond_idx if condition and grid[i].state!="wall"]

    # TODO: Implement "isCoordinateIn" method