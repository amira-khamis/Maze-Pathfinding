import heapq

class UCS:
    def __init__(self):
        self.explored_nodes = []

    def solve(self, maze):
        start = maze.start
        goal = maze.goal

        frontier = [(0, start, None)]  
        came_from = {start: None}
        cost_so_far = {start: 0}
        self.explored_nodes = []

        while frontier:
            frontier.sort(key=lambda x: x[0]) 
            cost, current, parent = frontier.pop(0)
            self.explored_nodes.append(current)
            came_from[current] = parent

            if current == goal:
                path = []
                node = goal
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                return path[::-1]

            x, y = current
            for neighbor in maze.get_neighbors(x, y):
                new_cost = cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    frontier.append((new_cost, neighbor, current))

        print("[UCS] No path found")
        return []
