### A Python visual tool for drawing different kinds of maze configurations and testing different algorithms to solve them.
<img src="https://github.com/Renua-Meireles/PathFinding/blob/master/screenshots/draw_and_run.gif" width="420" height="280" />

### Features
- Run different search algorithms to solve the drawn maze. Currently available algorithms:

**A\* Search**

<img src="https://github.com/Renua-Meireles/PathFinding/blob/master/screenshots/aStar.gif" width="300" height="200" />

**Bread-First Search**

<img src="https://github.com/Renua-Meireles/PathFinding/blob/master/screenshots/bread-first.gif" width="300" height="200" />

**Depth-First Search**

<img src="https://github.com/Renua-Meireles/PathFinding/blob/master/screenshots/depth-first.gif" width="300" height="200" />

 
- Freely draw the shapes you want
You can create blocks by **right-clicking** on nodes.
<img src="https://github.com/Renua-Meireles/PathFinding/blob/master/screenshots/ss01.png" width="420" height="280" />

- Delete unwanted blocks
You can create blocks by **left-clicking** on nodes.
<img src="https://github.com/Renua-Meireles/PathFinding/blob/master/screenshots/draw.gif" width="420" height="280" />
 
### Customize
- Window

You can change several parameters at main.py file. Currently GUI class supports the following parameters: 
```
width : int, optional
    The width of the window, by default 1000
height : int, optional
    The height of the window, by default 700
padding : tuple, optional
    The left, right, bottom, and top respective paddings of the window, by default (0, 0, 0, 0)
gap : int, optional
    The gap between the nodes, by default 1
node_size : int, optional
    The size of the node, by default 25
fps : int, optional
    The amount of frames per second, by default 120
 ```
In main.py file you can edit the GUI object creation passing as many parameters as you want, e.g.:
```python
...
gui_fps = 120
path_finding_fps = 30 # FPS used during the PathFinding process.
gui = Gui(width=400, height=200, padding=(0, 0, 5, 5), gap=5, node_size=50, fps=gui_fps)
...
```
- Keyboard keys mapping

Currently, you can start an algorithm by pressing **A for A***, **D for Depth-First**, and **B for Bread-First**, which's defined in main.py file:
```python
...
search_mapping = {
    pygame.K_a: aStar,
    pygame.K_d: depthFirst,
    pygame.K_b: breadthFirstSearch,
}
...
```
You can change this freely by replacing pygame constants with other ones available like 
**pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, ..., etc**. See all available constants at [pygame's documentation](https://www.pygame.org/docs/ref/key.html)

- Colors

You can add new colors for each block function just by following **two steps**
1- Adding new constant RGB Tuple in colors.py file (There also you will find the existent ones)
```python
...
CUSTOM_COLOR = (122, 42, 177)
```
2- Editing the node function in node.py file just by calling the name of your new color:
```python
self.state_color_map = {
    "empty": colors.CUSTOM_COLOR,
    "wall": colors.BLACK,
    "start point": colors.GREEN,
    "end point": colors.RED,
    "path": colors.TURQUOISE,
    "visited": colors.ORANGE,
    "watch": colors.PURPLE
}
```
 
 ### About
Thanks for checking out this project!

This project was highly inspired by Cruickshank's A* algorithm explanation, check out his [work](https://morioh.com/p/cf0c6b11c848).
