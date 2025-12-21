from collections import deque

class BFS:
    def __init__(self):
        self.explored_nodes = []
    
    def solve(self, maze):
        """Solve maze using BFS algorithm"""
        start = maze.start
        goal = maze.goal
        grid = maze.grid
        
       
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
     
        queue = deque([start])
        visited = set([start])
        parent = {start: None}
        self.explored_nodes = [start]
        
        while queue:
            current = queue.popleft()
            
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
                
                if (0 <= nx < maze.width and 0 <= ny < maze.height and 
                    grid[ny][nx] == 0 and 
                    neighbor not in visited):
                    
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
                    self.explored_nodes.append(neighbor)
        
       
        print("[BFS] No path found")
        return []
