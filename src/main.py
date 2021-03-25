import pygame
from gui import Gui
from algorithms import aStar, depthFirst, breadthFirstSearch


def main():
    gui_fps = 120
    path_finding_fps = 30
    gui = Gui(fps = gui_fps)

    # Mapping the keys that triggers an algorithm initialization
    search_mapping = {
        pygame.K_a: aStar,
        pygame.K_d: depthFirst,
        pygame.K_b: breadthFirstSearch,
    }

    start_node = None
    end_node = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui.close()
                
            if pygame.mouse.get_pressed()[0]: # LEFT MOUSE BUTTON
                mouse_xy = pygame.mouse.get_pos()
                start_node, end_node = gui.setNodeColor(mouse_xy, start_node, end_node)


            if pygame.mouse.get_pressed()[2]: # RIGHT MOUSE BUTTON
                mouse_xy = pygame.mouse.get_pos()
                start_node, end_node = gui.resetNodeColor(mouse_xy, start_node, end_node)
            
            if event.type == pygame.KEYDOWN:
                # Look for the keys that triggers an algorithm initialization
                if event.key in search_mapping.keys():
                    if start_node and end_node:
                        gui.updateNodeNeighbors()
                        gui.reset(exeptions=["wall", "start point", "end point"])
                        search = search_mapping[event.key]
                        gui.fps = path_finding_fps
                        search(gui, start_node, end_node)
                        gui.fps = gui_fps

                # Look for the keys that resets all blocks
                if event.key == pygame.K_SPACE:
                    start_node, end_node = None, None
                    gui.reset()

                # Look for the keys that resets all blocks except the maze configuration
                if event.key == pygame.K_c:
                    gui.reset(exeptions=["wall", "start point", "end point"])

        gui.updateContents()

if __name__ == '__main__':
    main()