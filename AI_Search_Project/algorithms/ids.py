class IDS:
    def __init__(self):
        self.explored_nodes = []

    def solve(self, maze):
        start = maze.start
        goal = maze.goal
        max_depth = maze.width * maze.height

        for depth in range(max_depth):
            visited = set()
            parent = {start: None}
            self.explored_nodes = [start]

            found = self.dls(
                maze,
                start,
                goal,
                depth,
                visited,
                parent
            )

            if found:
                path = []
                current = goal
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

        print("[IDS] No path found")
        return []

    def dls(self, maze, current, goal, depth, visited, parent):
        if current == goal:
            return True

        if depth == 0:
            return False

        visited.add(current)

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        x, y = current

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if (
                0 <= nx < maze.width and
                0 <= ny < maze.height and
                maze.grid[ny][nx] == 0 and
                neighbor not in visited
            ):
                parent[neighbor] = current
                self.explored_nodes.append(neighbor)

                if self.dls(
                    maze,
                    neighbor,
                    goal,
                    depth - 1,
                    visited,
                    parent
                ):
                    return True

        return False
