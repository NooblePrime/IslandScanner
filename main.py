import matplotlib.pyplot as plt
import numpy as np
from islandStructure import Grid, IslandNode
from matplotlib.colors import ListedColormap
from pprint import pprint

def discover_island(x: int, y: int, grid: Grid, nodes=None) -> list[tuple[int, int]]:
    if nodes is None:
        nodes = []
    if (
        x < 0 or y < 0 or x >= grid.rows or y >= grid.cols or
        not isinstance(grid.grid[x][y], IslandNode) or grid.grid[x][y].discovered
    ):
        return nodes
    if (x, y) in nodes:
        return nodes
    nodes.append((x, y))
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            discover_island(x + i - 1, y + j - 1, grid, nodes)
    return nodes


def update_grid(plot, scanner_pos):
    grid_data = np.zeros((plot.rows, plot.cols))
    for r in range(plot.rows):
        for c in range(plot.cols):
            if [c, r] == scanner_pos:
                grid_data[r, c] = 2
            elif isinstance(plot.grid[r][c], IslandNode) and plot.grid[r][c].discovered:
                grid_data[r, c] = 1
            elif isinstance(plot.grid[r][c], IslandNode) and not plot.grid[r][c].discovered:
                grid_data[r, c] = 3
            else:
                grid_data[r, c] = 0
    plt.cla()
    if not any(
                isinstance(plot.grid[r][c], IslandNode) and not plot.grid[r][c].discovered
                for r in range(plot.rows)
                for c in range(plot.cols)
            ):
        plt.imshow(grid_data, cmap=ListedColormap(["blue", "green", "magenta"]))
    else:
        plt.imshow(grid_data, cmap=ListedColormap(["blue", "green", "magenta", "black"]))

def main():
    plot = Grid(30, 20)
    plot.populate(5, 10)

    discovered_islands = []
    for row in range(plot.rows):
        for col in range(plot.cols):
            if isinstance(plot.grid[row][col], IslandNode) and not plot.grid[row][col].discovered:
                new_island = discover_island(row, col, plot)
                for node in new_island:
                    plot.grid[node[0]][node[1]].discover()
                    update_grid(plot, [col, row])
                    plt.pause(0.05)
                discovered_islands.append(new_island)
            update_grid(plot, [col, row])
            plt.pause(0.01)
    pprint(discovered_islands)

if __name__ == "__main__":
    main()