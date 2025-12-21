import time
import sys
import math  
import matplotlib.pyplot as plt
from maze import Maze, MazeVisualizer
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.ids import IDS
from algorithms.ucs import UCS
from algorithms.astar import AStar

print("=" * 60)
print("AI SEARCH ALGORITHMS COMPARISON")
print("=" * 60)

def run_algorithms_on_maze(maze_obj):
    algorithms = {
        "BFS": BFS(),
        "DFS": DFS(),
        "IDS": IDS(),
        "UCS": UCS(),
        "AStar": AStar()
    }

    results = {}
    print("\nRUNNING ALGORITHMS...")
    
    for name, solver in algorithms.items():
        path = solver.solve(maze_obj)
        
        if path is not None and len(path) > 0:
            explored = len(solver.explored_nodes) if hasattr(solver, 'explored_nodes') else 0
            results[name] = {
                "solver": solver,
                "path": path,
                "path_length": len(path),
                "explored_nodes": explored,
                "exec_time_ms": 0,
                "path_cost": 0,
                "memory": 0,
                "is_optimal": False,
                "success_rate": 0.0
            }

    print("\nCALCULATING EXECUTION TIMES AND METRICS...")
    
    for name, data in results.items():
        solver = data["solver"]

        total_time = 0
        runs = 10 
        
        for _ in range(runs):
            start_time = time.perf_counter_ns()
            solver.solve(maze_obj)
            end_time = time.perf_counter_ns()
            total_time += (end_time - start_time)
        
        avg_time_ns = total_time / runs
        avg_time_ms = avg_time_ns / 1_000_000
        results[name]["exec_time_ms"] = avg_time_ms

        path = data["path"]
        path_cost = 0
        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            path_cost += abs(x1-x2) + abs(y1-y2)
        
        results[name]["path_cost"] = path_cost

        explored = data["explored_nodes"]
        if name == "BFS":
            memory = explored * 2 
        elif name == "DFS":
            memory = explored * 1.5
        elif name == "IDS":
            memory = explored * 1.2
        elif name == "UCS":
            memory = explored * 2.5 
        elif name == "AStar":
            memory = explored * 3
        
        results[name]["memory"] = memory
        
        is_optimal = name in ["BFS", "UCS", "AStar"] 
        results[name]["is_optimal"] = is_optimal

        success_rate = 100.0 if path else 0.0
        results[name]["success_rate"] = success_rate
        
        print(f"{name}: {data['path_length']} steps | Cost: {path_cost} | "
              f"{explored} explored | Time: {avg_time_ms:.2f} ms")

    return results

def get_best_algorithm(results):
    scores = {}
    
    for name, data in results.items():
        score = 0
        
        min_path = min(r["path_length"] for r in results.values())
        min_time = min(r["exec_time_ms"] for r in results.values())
        min_explored = min(r["explored_nodes"] for r in results.values())
        min_cost = min(r["path_cost"] for r in results.values())
        min_memory = min(r["memory"] for r in results.values())

        if data["path_length"] == min_path:
            score += 20
        if data["exec_time_ms"] == min_time:
            score += 20
        if data["explored_nodes"] == min_explored:
            score += 15
        if data["path_cost"] == min_cost:
            score += 20
        if data["memory"] == min_memory:
            score += 15
        if data["is_optimal"]:
            score += 10
        
        scores[name] = score
    
    return max(scores, key=scores.get)

def exit_program():
    plt.close("all")
    sys.exit(0)

maze = Maze(width=20, height=12)
results = run_algorithms_on_maze(maze)

while True:
    print("\n" + "="*60)
    print("MAZE INFO")
    print(f"Start: {maze.start} | Goal: {maze.goal}")
    print("="*60)

    menu_map = {}
    counter = 1
    
    for name, data in results.items():
        print(f"{counter}. View {name} Solution "
              f"({data['path_length']} steps | Cost: {data['path_cost']} | "
              f"Time: {data['exec_time_ms']:.2f} ms)")
        menu_map[counter] = name
        counter += 1
    
    print(f"{counter}. View ALL Solutions")
    menu_map[counter] = "ALL"
    counter += 1
    
    print(f"{counter}. View BEST Algorithm")
    menu_map[counter] = "BEST"
    counter += 1
    
    print(f"{counter}. View Algorithm Comparison")
    menu_map[counter] = "COMPARE"
    counter += 1
    
    print(f"{counter}. Exit Program")
    menu_map[counter] = "EXIT"
    
    print("-" * 60)
    
    try:
        choice = int(input("Select option: "))
    except:
        continue
    
    action = menu_map.get(choice)
    
    if action in results:
        data = results[action]
        visualizer = MazeVisualizer(maze)
        visualizer.animate(
            data["path"],
            algorithm_name=f"{action} Algorithm"
        )
    
    elif action == "ALL":
        for name, data in results.items():
            visualizer = MazeVisualizer(maze)
            visualizer.animate(
                data["path"],
                algorithm_name=f"{name} Algorithm"
            )
    
    elif action == "BEST":
        best = get_best_algorithm(results)
        data = results[best]
        visualizer = MazeVisualizer(maze)
        visualizer.animate(
            data["path"],
            algorithm_name=f"BEST Algorithm ({best})"
        )
    
    elif action == "COMPARE":
        print("\n" + "="*80)
        print("ALGORITHM COMPARISON")
        print("="*80)
        print(f"{'Algorithm':<10} {'Steps':<8} {'Cost':<8} {'Explored':<10} "
              f"{'Time(ms)':<10} {'Memory':<10} {'Optimal':<10} {'Success':<10}")
        print("-"*80)
        
        for name, data in results.items():
        
            min_path = min(r["path_length"] for r in results.values())
            min_time = min(r["exec_time_ms"] for r in results.values())
            min_explored = min(r["explored_nodes"] for r in results.values())
            min_cost = min(r["path_cost"] for r in results.values())
            min_memory = min(r["memory"] for r in results.values())
            
            score = 0
            if data["path_length"] == min_path:
                score += 20
            if data["exec_time_ms"] == min_time:
                score += 20
            if data["explored_nodes"] == min_explored:
                score += 15
            if data["path_cost"] == min_cost:
                score += 20
            if data["memory"] == min_memory:
                score += 15
            if data["is_optimal"]:
                score += 10
            
            print(
                f"{name:<10} "
                f"{data['path_length']:<8} "
                f"{data['path_cost']:<8} "
                f"{data['explored_nodes']:<10} "
                f"{data['exec_time_ms']:<10.2f} "
                f"{data['memory']:<10.0f} "
                f"{'YES' if data['is_optimal'] else 'NO':<10} "
                f"{data['success_rate']:<10.1f}%"
            )
    
    elif action == "EXIT":
        exit_program()
