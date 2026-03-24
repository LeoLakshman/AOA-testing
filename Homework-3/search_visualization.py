import matplotlib.pyplot as plt
import networkx as nx
from search import depthFirstSearch, breadthFirstSearch, uniformCostSearch
from game import Directions
import util

# Define a simple graph search problem for visualization
class SimpleGraphProblem:
    def __init__(self):
        self.start = 'A'
        self.goal = 'G'
        # Graph: A -> B, A -> G, A -> D, B -> D, D -> G
        self.graph = {
            'A': [('B', '0:A->B', 1.0), ('G', '1:A->G', 2.0), ('D', '2:A->D', 4.0)],
            'B': [('D', '0:B->D', 8.0)],
            'D': [('G', '0:D->G', 16.0)],
            'G': []
        }

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state == self.goal

    def getSuccessors(self, state):
        return self.graph.get(state, [])

    def getCostOfActions(self, actions):
        return 0  # Not used for unweighted search

def visualize_search_tree(problem, algorithm_name, algorithm_func):
    """Visualize the search tree for a given algorithm"""

    # Create the graph
    G = nx.DiGraph()

    # Add nodes and edges from the problem
    for node, successors in problem.graph.items():
        for successor, action, cost in successors:
            G.add_edge(node, successor, action=action, cost=cost)

    # Get the solution path
    solution = algorithm_func(problem)

    # Create positions for nodes
    pos = {
        'A': (0, 0),
        'B': (-1, -1),
        'D': (1, -1),
        'G': (0, -2)
    }

    plt.figure(figsize=(12, 8))

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=2000, font_size=16, font_weight='bold',
            arrows=True, arrowsize=20, edge_color='gray', width=2)

    # Highlight the solution path
    if solution:
        path_edges = []
        current = problem.getStartState()
        for action in solution:
            # Find the successor for this action
            for succ, act, cost in problem.getSuccessors(current):
                if act == action:
                    path_edges.append((current, succ))
                    current = succ
                    break

        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                             edge_color='red', width=4, arrows=True, arrowsize=25)

    # Add edge labels
    edge_labels = {(u, v): f"{d['action']}\n({d['cost']})" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)

    plt.title(f'{algorithm_name} Search Tree\nSolution Path: {" -> ".join([problem.getStartState()] + solution) if solution else "No solution"}')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'{algorithm_name.lower().replace(" ", "_")}_search_tree.png', dpi=300, bbox_inches='tight')
    plt.show()

def visualize_maze_path():
    """Visualize the path on a simple maze"""
    # Create a simple maze layout
    maze = [
        ['%', '%', '%', '%', '%', '%', '%'],
        ['%', ' ', ' ', ' ', ' ', ' ', '%'],
        ['%', ' ', '%', '%', '%', ' ', '%'],
        ['%', ' ', ' ', ' ', '%', ' ', '%'],
        ['%', '%', '%', ' ', '%', ' ', '%'],
        ['%', ' ', ' ', ' ', ' ', ' ', '%'],
        ['%', '%', '%', '%', '%', '%', '%']
    ]

    # Pacman start at (1,1), goal at (5,5)
    start = (1, 1)
    goal = (5, 5)

    # Simple path: right, right, down, down, right, right
    path = [(1,1), (1,2), (1,3), (2,3), (3,3), (4,3), (4,4), (4,5), (5,5)]

    plt.figure(figsize=(8, 8))

    # Draw maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '%':
                plt.fill([j, j+1, j+1, j], [len(maze)-i-1, len(maze)-i-1, len(maze)-i, len(maze)-i],
                        color='black')
            else:
                plt.fill([j, j+1, j+1, j], [len(maze)-i-1, len(maze)-i-1, len(maze)-i, len(maze)-i],
                        color='white', edgecolor='gray', linewidth=1)

    # Draw path
    path_x = [p[1] + 0.5 for p in path]
    path_y = [len(maze) - p[0] - 0.5 for p in path]
    plt.plot(path_x, path_y, 'r-', linewidth=3, marker='o', markersize=8, markerfacecolor='yellow')

    # Mark start and goal
    plt.plot(start[1] + 0.5, len(maze) - start[0] - 0.5, 'go', markersize=15, label='Start')
    plt.plot(goal[1] + 0.5, len(maze) - goal[0] - 0.5, 'ro', markersize=15, label='Goal')

    plt.title('Pacman Path Visualization')
    plt.legend()
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('pacman_path_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    problem = SimpleGraphProblem()

    print("Visualizing DFS Search Tree...")
    visualize_search_tree(problem, "Depth First Search", depthFirstSearch)

    print("Visualizing BFS Search Tree...")
    visualize_search_tree(problem, "Breadth First Search", breadthFirstSearch)

    print("Visualizing UCS Search Tree...")
    visualize_search_tree(problem, "Uniform Cost Search", uniformCostSearch)

    print("Visualizing Maze Path...")
    visualize_maze_path()

    print("Visualizations saved as PNG files!")