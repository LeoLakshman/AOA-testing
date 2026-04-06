import util
from game import Directions
from typing import List

class SearchProblem:
    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()  

    def getCostOfActions(self, actions):
        util.raiseNotDefined() 




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))

    visited = set()

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)

            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    frontier.push((successor, actions + [action]))

    return []

dfs = depthFirstSearch

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))

    visited = set()

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)

            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    frontier.push((successor, actions + [action]))

    return []

bfs = breadthFirstSearch

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    start_state = problem.getStartState()

    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), 0)

    best_cost = {start_state: 0}

    while not frontier.isEmpty():
        state, actions, cost_so_far = frontier.pop()

        if cost_so_far > best_cost.get(state, float('inf')): 
            continue

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost
            if new_cost < best_cost.get(successor, float('inf')):
                best_cost[successor] = new_cost
                frontier.push((successor, actions + [action], new_cost), new_cost)

    return []

ucs = uniformCostSearch

def nullHeuristic(state, problem=None):
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    start_state = problem.getStartState()

    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), heuristic(start_state, problem))

    best_cost = {start_state: 0}

    while not frontier.isEmpty():
        state, actions, cost_so_far = frontier.pop()

        if cost_so_far > best_cost.get(state, float('inf')):
            continue

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost

            if new_cost < best_cost.get(successor, float('inf')):
                best_cost[successor] = new_cost
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, actions + [action], new_cost), priority)

    return []

astar = aStarSearch
