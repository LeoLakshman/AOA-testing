
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
    down = Directions.SOUTH
    left = Directions.WEST
    return [down, down, left, down, left, left, down, left]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:

    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))

    explored = set()

    while not frontier.isEmpty():
        state, route = frontier.pop()

        if problem.isGoalState(state):
            return route

        if state not in explored:
            explored.add(state)

            for succ_state, action, step_cost in problem.getSuccessors(state):
                if succ_state not in explored:
                    frontier.push((succ_state, route + [action]))

    return []

dfs = depthFirstSearch