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
    south = Directions.SOUTH
    west = Directions.WEST
    return  [south, south, west, south, west, west, south, west]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    open_list = util.Stack()
    open_list.push((problem.getStartState(), []))

    explored = set()

    while not open_list.isEmpty():
        node, path = open_list.pop()

        if problem.isGoalState(node):
            return path

        if node not in explored:
            explored.add(node)

            for child, direction, cost in problem.getSuccessors(node):
                if child not in explored:
                    open_list.push((child, path + [direction]))

    return []

dfs = depthFirstSearch

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    open_list = util.Queue()
    open_list.push((problem.getStartState(), []))

    explored = set()

    while not open_list.isEmpty():
        node, path = open_list.pop()

        if problem.isGoalState(node):
            return path

        if node not in explored:
            explored.add(node)

            for child, direction, cost in problem.getSuccessors(node):
                if child not in explored:
                    open_list.push((child, path + [direction]))

    return []

bfs = breadthFirstSearch

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    initial_state = problem.getStartState()

    pq = util.PriorityQueue()
    pq.push((initial_state, [], 0), 0)

    min_cost = {initial_state: 0}

    while not pq.isEmpty():
        current, path, total_cost = pq.pop()

        if total_cost > min_cost.get(current, float('inf')):
            continue

        if problem.isGoalState(current):
            return path

        for neighbor, move, edge_cost in problem.getSuccessors(current):
            updated_cost = total_cost + edge_cost
            if updated_cost < min_cost.get(neighbor, float('inf')):
                min_cost[neighbor] = updated_cost
                pq.push((neighbor, path + [move], updated_cost), updated_cost)

    return []

ucs = uniformCostSearch
