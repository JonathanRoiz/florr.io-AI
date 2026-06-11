from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from typing import Any

def astar(binary, start, end) -> (tuple[Any, int] | tuple[list, int]):
    # pathfinding expects 1=walkable, 0=wall
    grid = Grid(matrix=binary // 255)  # convert 0/255 to 0/1
    
    start_node = grid.node(start[0], start[1])
    end_node = grid.node(end[0], end[1])
    
    finder = AStarFinder()
    path, _ = finder.find_path(start_node, end_node, grid)
    
    return path

def find_nearest_walkable(binary, pos):
    x, y = pos
    grid_matrix = binary // 255
    
    if grid_matrix[y][x] == 1:
        return pos  # already walkable
    
    # Spiral outward until we find a walkable pixel
    for radius in range(1, 20):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < binary.shape[1] and 0 <= ny < binary.shape[0]:
                    if grid_matrix[ny][nx] == 1:
                        return (nx, ny)
    return None  # no walkable pixel found nearby
