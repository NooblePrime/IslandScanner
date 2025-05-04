from random import randint, choice
from colorama import Fore, Style
class IslandNode:
    def __init__(self, discovered=False):
        self.discovered = discovered
    
    def discover(self):
        self.discovered = True

class Grid:
    def __init__(self, cols: int, rows: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    class Island:
        def __init__(self, grid_instance, source_x, source_y):
            self.grid_instance = grid_instance
            self.source_x = source_x
            self.source_y = source_y
            self.grid_instance.grid[source_x][source_y] = IslandNode()

        def spread(self, size: int):
            nodes = [[self.source_x, self.source_y]]
            queue = [[self.source_x, self.source_y]]
            for _ in range(size):
                if not queue:
                    break
                spreading_node = queue.pop(0)
                spread_x = spreading_node[0]
                spread_y = spreading_node[1]
                possible_spots = []
                for i in range(3):
                    for j in range(3):
                        spot = [spread_x + i - 1, spread_y + j - 1]
                        if (
                            0 <= spot[0] < self.grid_instance.rows
                            and 0 <= spot[1] < self.grid_instance.cols
                            and self.grid_instance.grid[spot[0]][spot[1]] is None
                        ):
                            possible_spots.append(spot)
                if not possible_spots:
                    continue
                spot = choice(possible_spots)
                self.grid_instance.grid[spot[0]][spot[1]] = IslandNode()
                nodes.append(spot)
                queue.append(spot)

    def populate(self, n: int, size: int):
        for _ in range(n):
            retry = True
            while retry:
                x = randint(0, self.rows - 1)
                y = randint(0, self.cols - 1)
                if self.grid[x][y] is not None:
                    continue
                new_island = self.Island(self, x, y)
                self.grid[x][y] = new_island
                new_island.spread(size)
                retry = False

    def display(self, scanner=[0, 0]):
        print(self.get_display(scanner) + '\n')

    def get_display(self, scanner=[0, 0]):
        display_string = ''
        for row_index, row in enumerate(self.grid):
            for col_index, node in enumerate(row):
                if [col_index, row_index] == scanner:
                    display_string += f'{Fore.MAGENTA}██{Style.RESET_ALL}'
                elif isinstance(node, IslandNode):
                    if node.discovered:
                        display_string += f'{Fore.GREEN}██{Style.RESET_ALL}'
                    else:
                        display_string += f'{Fore.BLACK}██{Style.RESET_ALL}'
                else:
                    display_string += f'{Fore.BLUE}██{Style.RESET_ALL}'
            display_string += '\n'
        return display_string