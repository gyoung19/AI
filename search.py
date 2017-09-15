# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class Node:
    def __init__(self, value = None, parent = None):
        self.value = value
        self.parent = parent

    def getParent(self):
        return self.parent

    def getValue(self):
        return self.value

    def getLineage(self):
        if self.parent is None:
            return []
        else:
            return self.parent.getLineage() + [self]


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch_dirty(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
   
    start = problem.getStartState()
    fringe, explored = util.Stack(), []

    for nextNode in problem.getSuccessors(start):
        fringe.push([nextNode, [nextNode[1]]])


    while not fringe.isEmpty():
        currentNode, actionPath = fringe.pop()
        
        if problem.isGoalState(currentNode[0]):
            print "tada!"
            print actionPath
            return actionPath
        explored += currentNode
        for successor in problem.getSuccessors(currentNode[0]):
            if successor[0] not in explored:
                fringe.push([successor, actionPath + [successor[1]]])
                

def depthFirstSearch(problem): 
    startState = problem.getStartState()
    startNode = Node([startState, None, None], None) 
    fringe, explored = util.Stack(), set([startState]) 
    # fringe contains Node objects, whose getValue() gives [state, action, stepcost]
    # explored contains visited STATES

    if problem.isGoalState(startState):
        return []

    for successor in problem.getSuccessors(startState):
        fringe.push(Node(successor, parent = startNode))


    while not fringe.isEmpty():
        currentNode = fringe.pop()
        currentState = currentNode.getValue()[0]

        if problem.isGoalState(currentState):
            lineage = currentNode.getLineage()
            actions = []
            for ancestor in lineage:
                actions.append(ancestor.getValue()[1])
            
            return actions

        explored.add(currentState)
        for successor in problem.getSuccessors(currentState):
            if successor[0] not in explored:
                fringe.push(Node(successor, parent = currentNode))
                

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    startState = problem.getStartState()
    startNode = Node([startState, None, None], None) 
    fringe, explored = util.Queue(), set([startState]) 
    # fringe contains Node objects, whose getValue() gives [state, action, stepcost]
    # explored contains visited STATES

    if problem.isGoalState(startState):
        return []

    for successor in problem.getSuccessors(startState):
        fringe.push(Node(successor, parent = startNode))
        explored.add(successor[0]) #?? not sure yet


    while not fringe.isEmpty():
        currentNode = fringe.pop()
        currentState = currentNode.getValue()[0]

        if problem.isGoalState(currentState):
            lineage = currentNode.getLineage()
            actions = []
            for ancestor in lineage:
                actions.append(ancestor.getValue()[1])
            #print actions
            return actions

        #explored.add(currentState)
        for successor in problem.getSuccessors(currentState):
            if successor[0] not in explored:
                #print str(explored) + ' and ' + str(successor[0]) #for debugging
                explored.add(successor[0])
                fringe.push(Node(successor, parent = currentNode))
                

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    startNode = Node([startState, None, None], None) 
    fringe, explored = util.PriorityQueue(), set([startState])  

    # fringe contains Node objects, whose getValue() gives [state, action, stepcost]
    # explored contains visited STATES

    if problem.isGoalState(startState):
        return []

    for successor in problem.getSuccessors(startState):
        totalPathCost = 0 + successor[2] # being at startNode takes 0 cost
        updatedSuccessor = [successor[0], successor[1], totalPathCost]
        fringe.push(Node(updatedSuccessor, parent = startNode), totalPathCost)
        explored.add(successor[0]) #?? not sure yet


    while not fringe.isEmpty():
        currentNode = fringe.pop()
        currentState = currentNode.getValue()[0]
        
        
        if problem.isGoalState(currentState):
            lineage = currentNode.getLineage()
            actions = []            
            for ancestor in lineage:
                actions.append(ancestor.getValue()[1])
            return actions
        
        
        #explored.add(currentState)
        for successor in problem.getSuccessors(currentState):
            if successor[0] not in explored:
                totalPathCost = currentNode.getValue()[2] + successor[2]
                updatedSuccessor = [successor[0], successor[1], totalPathCost]
                print totalPathCost

                """
                # redundant
                if problem.isGoalState(successor[0]):
                    lineage = currentNode.getLineage()
                    actions = []
                    
                    for ancestor in lineage:
                        actions.append(ancestor.getValue()[1])

                    actions.append(currentNode.getValue()[1])
                    #print actions
                    return actions
                """

                fringe.push(Node(updatedSuccessor, parent = currentNode), totalPathCost)
                explored.add(successor[0])
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # T: So it seems heuristic functions take (state, problem)
    #   and return the cost for that state.
    startState = problem.getStartState()
    startNode = Node([startState, None, None], None) 
    fringe, explored = util.PriorityQueue(), set([]) 
    # fringe contains Node objects, whose getValue() gives [state, action, stepcost]
    # explored contains visited STATES

    for successor in problem.getSuccessors(startState):
        totalPathCost = 0 + successor[2] # being at startNode takes 0 cost
        totalCost = totalPathCost + heuristic(successor[0], problem)
        fringe.push(Node(successor, parent = startNode), totalCost)
        explored.add(successor[0])


    while not fringe.isEmpty():
        currentNode = fringe.pop()
        #actions.append(currentNode[1])
        if problem.isGoalState(currentNode.getValue()[0]):
            lineage = currentNode.getLineage()
            actions = []
            for ancestor in lineage:
                actions.append(ancestor.getValue()[1])
            #print actions
            return actions

        explored.add(currentNode.getValue()[0])
        for successor in problem.getSuccessors(currentNode.getValue()[0]):
            if successor[0] not in explored:
                totalPathCost = currentNode.getValue()[2] + successor[2]
                totalCost = totalPathCost + heuristic(successor[0], problem)
                fringe.push(Node(successor, parent = currentNode), totalCost)
                explored.add(successor[0])
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
