"""
INTERACTIVE DFS VISUALIZATION WITH TKINTER GRAPHICS
====================================================

This script provides a visual, interactive explanation of how DFS works.
Watch as DFS explores a maze in real-time!

FEATURES:
- Visual representation of DFS exploration
- Step-by-step animation
- Interactive controls (Play, Step, Reset)
- Color-coded states (visited, exploring, goal)
- Real-time stack visualization

RUN THIS WITH:
    python dfs_visualization.py
"""

import tkinter as tk
from tkinter import messagebox, ttk
import time
from collections import deque


class SimpleMaze:
    """A simple maze for visualization"""
    def __init__(self):
        # Grid layout: 1=wall, 0=passable
        self.grid = [
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0]
        ]
        self.start = (0, 0)
        self.goal = (4, 4)
        self.width = 5
        self.height = 5
    
    def get_neighbors(self, pos):
        """Get valid neighbors of a position"""
        x, y = pos
        neighbors = []
        # Try all 4 directions
        for dx, dy, direction in [(0, 1, 'Right'), (1, 0, 'Down'), 
                                   (0, -1, 'Left'), (-1, 0, 'Up')]:
            nx, ny = x + dx, y + dy
            # Check bounds and not a wall
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] == 0:
                    neighbors.append(((nx, ny), direction))
        return neighbors


class DFSVisualizer:
    """Tkinter visualization of DFS algorithm"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DFS Algorithm Visualization - Interactive Learning")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2c3e50")
        
        self.maze = SimpleMaze()
        self.cell_size = 60
        self.animation_speed = 500  # milliseconds
        
        # DFS state
        self.stack = []
        self.visited = set()
        self.path = []
        self.current = None
        self.exploring = False
        self.done = False
        
        # Setup UI
        self.setup_ui()
        self.reset_dfs()
    
    def setup_ui(self):
        """Create the user interface"""
        # Top control panel
        control_frame = tk.Frame(self.root, bg="#34495e", height=80)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(control_frame, 
                               text="🔍 DEPTH-FIRST SEARCH (DFS) VISUALIZATION",
                               font=("Arial", 16, "bold"), 
                               fg="white", bg="#34495e")
        title_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg="#34495e")
        button_frame.pack(pady=10)
        
        self.step_btn = tk.Button(button_frame, text="📍 STEP", 
                                  command=self.step_dfs, 
                                  bg="#3498db", fg="white", 
                                  font=("Arial", 11, "bold"),
                                  padx=15, pady=8)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_btn = tk.Button(button_frame, text="▶️  AUTO PLAY", 
                                  command=self.auto_play, 
                                  bg="#27ae60", fg="white",
                                  font=("Arial", 11, "bold"),
                                  padx=15, pady=8)
        self.auto_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(button_frame, text="🔄 RESET", 
                             command=self.reset_dfs, 
                             bg="#e74c3c", fg="white",
                             font=("Arial", 11, "bold"),
                             padx=15, pady=8)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        info_btn = tk.Button(button_frame, text="ℹ️  INFO", 
                            command=self.show_info, 
                            bg="#9b59b6", fg="white",
                            font=("Arial", 11, "bold"),
                            padx=15, pady=8)
        info_btn.pack(side=tk.LEFT, padx=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side: Canvas for maze
        canvas_frame = tk.Frame(main_frame, bg="#34495e")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        maze_label = tk.Label(canvas_frame, text="MAZE EXPLORATION", 
                             font=("Arial", 12, "bold"), 
                             fg="white", bg="#34495e")
        maze_label.pack()
        
        self.canvas = tk.Canvas(canvas_frame, 
                                width=self.cell_size * self.maze.width,
                                height=self.cell_size * self.maze.height,
                                bg="white", highlightthickness=2,
                                highlightbackground="#2c3e50")
        self.canvas.pack(pady=10)
        
        # Right side: Info panels
        info_frame = tk.Frame(main_frame, bg="#34495e", width=350)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Stack visualization
        stack_label = tk.Label(info_frame, text="📚 STACK (To Explore)",
                              font=("Arial", 11, "bold"),
                              fg="white", bg="#34495e")
        stack_label.pack(pady=5)
        
        self.stack_text = tk.Text(info_frame, height=8, width=40,
                                 bg="#2c3e50", fg="#2ecc71",
                                 font=("Courier", 9),
                                 highlightthickness=1,
                                 highlightbackground="#3498db")
        self.stack_text.pack(padx=5, pady=5)
        
        # Visited set
        visited_label = tk.Label(info_frame, text="✓ VISITED (Explored)",
                                font=("Arial", 11, "bold"),
                                fg="white", bg="#34495e")
        visited_label.pack(pady=5)
        
        self.visited_text = tk.Text(info_frame, height=6, width=40,
                                   bg="#2c3e50", fg="#e74c3c",
                                   font=("Courier", 9),
                                   highlightthickness=1,
                                   highlightbackground="#3498db")
        self.visited_text.pack(padx=5, pady=5)
        
        # Status
        status_label = tk.Label(info_frame, text="📊 STATUS",
                               font=("Arial", 11, "bold"),
                               fg="white", bg="#34495e")
        status_label.pack(pady=5)
        
        self.status_text = tk.Text(info_frame, height=6, width=40,
                                  bg="#2c3e50", fg="#f39c12",
                                  font=("Courier", 9),
                                  highlightthickness=1,
                                  highlightbackground="#3498db")
        self.status_text.pack(padx=5, pady=5)
        
        # Update displays
        self.update_displays()
    
    def reset_dfs(self):
        """Reset DFS algorithm to initial state"""
        self.stack = [(self.maze.start, [self.maze.start])]
        self.visited = set()
        self.path = []
        self.current = None
        self.exploring = False
        self.done = False
        self.update_displays()
        self.draw_maze()
    
    def step_dfs(self):
        """Execute one step of DFS"""
        if self.done:
            messagebox.showinfo("Done", "Algorithm completed! Click RESET to try again.")
            return
        
        if not self.stack:
            self.done = True
            self.update_status("❌ NO SOLUTION FOUND")
            self.draw_maze()
            messagebox.showinfo("Complete", "No solution found! Stack is empty.")
            return
        
        # Pop from stack (LIFO - Last In First Out)
        current_pos, current_path = self.stack.pop()
        self.current = current_pos
        
        # Check if goal
        if current_pos == self.maze.goal:
            self.done = True
            self.path = current_path
            self.update_status(f"✅ GOAL FOUND!\nPath length: {len(current_path)}")
            self.draw_maze()
            return
        
        # Mark as visited
        if current_pos not in self.visited:
            self.visited.add(current_pos)
            
            # Get and push neighbors
            neighbors = self.maze.get_neighbors(current_pos)
            for neighbor_pos, direction in neighbors:
                if neighbor_pos not in self.visited:
                    new_path = current_path + [neighbor_pos]
                    self.stack.append((neighbor_pos, new_path))
        
        self.update_displays()
        self.draw_maze()
    
    def auto_play(self):
        """Automatically run DFS with animation"""
        if self.done:
            self.reset_dfs()
        
        self.animate_dfs()
    
    def animate_dfs(self):
        """Animate DFS exploration"""
        if self.done or not self.stack:
            return
        
        self.step_dfs()
        self.root.after(self.animation_speed, self.animate_dfs)
    
    def draw_maze(self):
        """Draw maze on canvas"""
        self.canvas.delete("all")
        
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                pos = (x, y)
                
                if self.maze.grid[y][x] == 1:
                    # Wall
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill="#2c3e50", outline="black")
                elif pos == self.maze.start:
                    # Start
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill="#3498db", outline="black", width=2)
                    self.canvas.create_text(x1 + self.cell_size//2, 
                                          y1 + self.cell_size//2,
                                          text="S", font=("Arial", 16, "bold"),
                                          fill="white")
                elif pos == self.maze.goal:
                    # Goal
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill="#2ecc71", outline="black", width=2)
                    self.canvas.create_text(x1 + self.cell_size//2, 
                                          y1 + self.cell_size//2,
                                          text="G", font=("Arial", 16, "bold"),
                                          fill="white")
                elif pos == self.current:
                    # Currently exploring
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill="#f39c12", outline="black", width=2)
                    self.canvas.create_text(x1 + self.cell_size//2, 
                                          y1 + self.cell_size//2,
                                          text="*", font=("Arial", 16, "bold"),
                                          fill="white")
                elif pos in self.visited:
                    # Visited
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill="#e74c3c", outline="black")
                else:
                    # Empty
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                fill="white", outline="gray")
    
    def update_displays(self):
        """Update info panels"""
        # Stack
        self.stack_text.config(state=tk.NORMAL)
        self.stack_text.delete(1.0, tk.END)
        for i, (pos, path) in enumerate(reversed(self.stack)):
            self.stack_text.insert(tk.END, f"[{i}] {pos}\n")
        self.stack_text.config(state=tk.DISABLED)
        
        # Visited
        self.visited_text.config(state=tk.NORMAL)
        self.visited_text.delete(1.0, tk.END)
        visited_list = sorted(list(self.visited))
        for pos in visited_list:
            self.visited_text.insert(tk.END, f"• {pos}\n")
        self.visited_text.insert(tk.END, f"\nTotal: {len(self.visited)}")
        self.visited_text.config(state=tk.DISABLED)
        
        # Status
        self.update_status(f"Queue size: {len(self.stack)}\nVisited: {len(self.visited)}")
    
    def update_status(self, text):
        """Update status panel"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, text)
        self.status_text.config(state=tk.DISABLED)
    
    def show_info(self):
        """Show information dialog"""
        info_text = """
DEPTH-FIRST SEARCH (DFS) EXPLANATION
=====================================

HOW IT WORKS:
1. Start with initial position in stack
2. Pop from stack (get MOST RECENT)
3. If it's the goal, SUCCESS!
4. Otherwise, mark as visited
5. Push all unvisited neighbors to stack
6. Repeat until finding goal or stack empty

KEY POINTS:
• STACK = LIFO (Last In First Out)
• Explore DEEP first, then backtrack
• Uses colors to show progress:
  - Blue: Start position
  - Green: Goal position
  - Orange: Currently exploring
  - Red: Already visited
  - White: Not yet visited

WHY DFS?
✓ Complete: Finds solution if exists
✓ Space efficient: One path deep at a time
✓ Simple to implement
✗ Not optimal: May find long solution

WATCH THE ANIMATION:
- See how stack grows as we discover neighbors
- See how visited set grows
- See current position changing
- Watch until goal is found!

Click STEP to manually control
Click AUTO PLAY for automatic animation
Click RESET to start over
"""
        messagebox.showinfo("DFS Algorithm Info", info_text)


def main():
    """Run the visualization"""
    root = tk.Tk()
    visualizer = DFSVisualizer(root)
    
    print("\n" + "="*60)
    print("🎨 DFS VISUALIZATION STARTED!")
    print("="*60)
    print("\n📚 INSTRUCTIONS:")
    print("1. Click STEP to explore one position at a time")
    print("2. Click AUTO PLAY to watch full animation")
    print("3. Check the info panels to see stack and visited states")
    print("4. Click INFO for detailed explanation")
    print("5. Click RESET to start over")
    print("\n" + "="*60 + "\n")
    
    root.mainloop()


if __name__ == "__main__":
    main()
