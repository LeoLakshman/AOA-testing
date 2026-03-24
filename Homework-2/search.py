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




def solve_tiny_maze(task: SearchProblem) -> List[Directions]:
    south_move = Directions.SOUTH
    west_move = Directions.WEST
    return  [south_move, south_move, west_move, south_move, west_move, west_move, south_move, west_move]

def depthFirstSearch(task: SearchProblem) -> List[Directions]:
    open_list = util.Stack()
    open_list.push((task.getStartState(), []))

    closed_list = set()

    while not open_list.isEmpty():
        current_node, moves_taken = open_list.pop()

        if task.isGoalState(current_node):
            return moves_taken

        if current_node not in closed_list:
            closed_list.add(current_node)

            for neighbor, direction, transition_cost in task.getSuccessors(current_node):
                if neighbor not in closed_list:
                    open_list.push((neighbor, moves_taken + [direction]))

    return []

dfs = depthFirstSearch

def breadthFirstSearch(task: SearchProblem) -> List[Directions]:
    open_list = util.Queue()
    open_list.push((task.getStartState(), []))

    closed_list = set()

    while not open_list.isEmpty():
        current_node, moves_taken = open_list.pop()

        if task.isGoalState(current_node):
            return moves_taken

        if current_node not in closed_list:
            closed_list.add(current_node)

            for neighbor, direction, transition_cost in task.getSuccessors(current_node):
                if neighbor not in closed_list:
                    open_list.push((neighbor, moves_taken + [direction]))

    return []

bfs = breadthFirstSearch
