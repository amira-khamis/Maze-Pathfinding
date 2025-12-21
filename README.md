# Maze Pathfinding

## Problem Description

Maze pathfinding involves navigating a grid from a **start position** to a **goal position**.  
The maze contains **walls (blocked cells)** and **free cells**.  
The objective is to find a valid path and compare how different search algorithms behave.

---

### Why This Problem?

- The maze has a well-defined **state space**
- You can encode the maze as a **graph**
- The **goal state** is explicit
- Algorithms behave differently 

## Overview

An educational Python project for visualizing and comparing classical AI search algorithms on a 2D maze.  
The project solves a maze by finding a path from a start position to a goal using different search strategies.  
Each algorithm is executed on the same maze to allow fair comparison.

## Implemented Algorithms

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Iterative Deepening Search (IDS)
- Uniform Cost Search (UCS)
- A* Search

## Key Features

- Interactive maze visualization using matplotlib
- Animated mouse moving toward the cheese (goal)
- Step-by-step path animation
- Comparison of algorithm performance
- Terminal-based menu for user interaction

## Performance Metrics

- Path length
- Number of explored nodes
- Execution time
- Path optimality
- Success Rate
- memory efficiency

## Requirements

- Python 3.6 or higher
- matplotlib

## Installation

Install required packages:
bash
pip install matplotlib

Usage

Run the main script:

bash
python main.py

Follow the on-screen instructions to:

1. Generate or load a maze
2. Choose a search algorithm
3. Visualize the pathfinding process

License

This project is for educational purposes.
