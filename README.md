Maze Pathfinding Algorithms Visualizer
An educational Python project for visualizing and comparing classical AI search algorithms on a 2D maze.

Overview
The project solves a maze by finding a path from a start position to a goal using different search strategies.
Each algorithm is executed on the same maze to allow fair comparison.

Implemented Algorithms
Breadth-First Search (BFS)
Depth-First Search (DFS)
Iterative Deepening Search (IDS)
Uniform Cost Search (UCS)
A* Search

Key Features
Interactive maze visualization using matplotlib
Animated mouse moving toward the cheese (goal)
Step-by-step path animation
Comparison of algorithm performance
Terminal-based menu for user interaction
Performance Metrics
Path length
Number of explored nodes
Execution time
Path optimality

 Project Structure
maze-project/
├── main.py
├── maze.py
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── ids.py
│   ├── ucs.py
│   └── astar.py
└── README.md

Requirements

Python 3.6 or higher
matplotlib

Installation
Install required packages:
pip install matplotlib

Usage
Run the main program:
python main.py


Use the menu to:
View individual algorithm solutions
Compare all algorithms
Generate a new maze
Exit the program


Trade-offs between speed, memory, and optimality

Happy Pathfinding! 🐭🧀
