# QUICK REFERENCE GUIDE: search.py Functions
# ============================================

## 3 KEY COMPONENTS

### 1. SearchProblem (Abstract Class)
```
Purpose: Defines interface for any searchable problem
Requires: 4 methods must be implemented
  - getStartState()          → Where do we start?
  - isGoalState(state)       → Is this the goal?
  - getSuccessors(state)     → What moves from here?
  - getCostOfActions(list)   → How expensive is this path?

Think: "Contract that says: implement these, and any algorithm can solve you"
```

### 2. tinyMazeSearch(problem)
```
❌ NOT RECOMMENDED - Hardcoded only for tinyMaze

Returns: Fixed sequence [south, south, west, south, west, west, south, west]

When to use: Testing/validation only
When NOT to: Real problems! Use DFS instead!

Lesson: Shows what to AVOID - memorizing answers vs learning algorithms
```

### 3. depthFirstSearch(problem) / dfs(problem)
```
✓✓✓ USE THIS ONE ✓✓✓

Type: Real general-purpose search algorithm
Data structure: Stack (LIFO = Last In First Out)
Strategy: Explore deep first, backtrack when stuck
Finds: ANY solution (not necessarily shortest)

Returns: List of actions from start to goal, or [] if no solution

Great for: Any maze, any graph, puzzles, navigation
Not great for: Finding shortest path (use BFS)

Time complexity: O(V + E) where V=states, E=edges
Space complexity: O(V)
```

---

## HOW DFS WORKS IN 4 STEPS

```
1. Push (start_state, [])      onto stack
2. While stack not empty:
   a. Pop (current, path)
   b. If current is GOAL:
      - Return path ✓ SUCCESS!
   c. If not visited before:
      - Mark as visited
      - For each neighbor not visited:
        * Push (neighbor, path + [action])
3. Return [] if no solution
```

---

## COMPARISON TABLE

| Property | tinyMaze | DFS | BFS |
|----------|----------|-----|-----|
| Type | Hardcoded | Algorithm | Algorithm |
| Works for | Only tiny | All problems | All problems |
| Finds shortest? | N/A | No | Yes |
| Complete? | Only tiny | Yes | Yes |
| Space efficient? | N/A | Better | Worse |
| Data structure | None | Stack | Queue |

---

## KEY ANALOGIES

### SearchProblem = GPS Interface
- GPS doesn't care if you're in NYC or Tokyo
- Just needs: start, goal, and roads
- Similarly, algorithms don't care about problem type
- Just need the 4 interface methods

### tinyMazeSearch = Memorizing Answers
- Works great for that specific test
- Fails completely on different test
- Teaches nothing about problem-solving

### DFS = Exploring a Cave
- Go down one tunnel fully
- Backtrack when blocked
- Try next tunnel
- Keep going until finding treasure

---

## RUNNING THE CODE

### Text mode (recommended):
```bash
cd /Users/leo/Desktop/Homework-1

# Various mazes
.venv/bin/python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs -t
.venv/bin/python pacman.py -l smallMaze -p SearchAgent -a fn=dfs -t
.venv/bin/python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs -t
```

### Output interpretation:
```
Path found with total cost of 10 in 0.0 seconds
Search nodes expanded: 15

= 10 moves to goal
= Searched 15 different states
= Very fast!
```

---

## UNDERSTANDING THE FILES

1. **search.py** - Original code with variable names changed
2. **search_annotated.py** - Same code with HEAVY commenting
3. **search_explanation.py** - Run this: `python search_explanation.py`
4. **Search_Algorithms_Explained.ipynb** - Jupyter notebook with visualizations

---

## WHAT TO MEMORIZE

```
SearchProblem      = Interface/contract
tinyMazeSearch     = DON'T do this (hardcoded)
depthFirstSearch   = DO use this (real algorithm)

Stack = LIFO (Last In First Out)
Queue = FIFO (First In First Out)

DFS uses Stack → Deep first behavior
BFS uses Queue → Breadth first behavior
```

---

## NEXT STEPS

1. Read search_explanation.py output
2. Study search_annotated.py carefully
3. Open Search_Algorithms_Explained.ipynb
4. Run pacman.py with different mazes
5. Try to implement BFS (similar but uses Queue)
6. Try to implement UCS (same but considers cost)

---

## COMMON MISTAKES

❌ Using tinyMazeSearch for real problems
❌ Thinking DFS finds shortest path
❌ Not implementing the 4 SearchProblem methods correctly
❌ Using Queue instead of Stack (that's BFS!)
❌ Not tracking visited states (infinite loops!)

✓ Always implement SearchProblem interface correctly
✓ Use depthFirstSearch for general problems
✓ Test with different mazes
✓ Understand why Stack (not Queue) makes it depth-first
