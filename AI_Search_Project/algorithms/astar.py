import heapq

class AStar:
    def __init__(self):
        self.explored_nodes = []

    def heuristic(self, node, goal):
        """Manhattan Distance heuristic"""
        x1, y1 = node
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def solve(self, maze):
        start = maze.start
        goal = maze.goal
        grid = maze.grid

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        open_list = []
        heapq.heappush(
            open_list,
            (self.heuristic(start, goal), 0, start)
        )

        parent = {start: None}
        g_cost = {start: 0}
        visited = set([start]) 
        self.explored_nodes = [start]

        while open_list:
            _, current_g, current = heapq.heappop(open_list)

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            x, y = current

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                
                if (
                    0 <= nx < maze.width and
                    0 <= ny < maze.height and
                    grid[ny][nx] == 0
                ):
                    tentative_g = current_g + 1

                    if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                        g_cost[neighbor] = tentative_g
                        f_cost = tentative_g + self.heuristic(neighbor, goal)

                        heapq.heappush(
                            open_list,
                            (f_cost, tentative_g, neighbor)
                        )

                        parent[neighbor] = current
                        
                        if neighbor not in visited:
                            visited.add(neighbor)
                            self.explored_nodes.append(neighbor)

        print("[A*] No path found")
        return []