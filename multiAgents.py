# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
#added code 
import sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if (action is "Stop"):
            return -1000
        bonus = 0

        newGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        closestGhostDistance = currentGameState.getWalls().height + currentGameState.getWalls().width # MAX
        #print newGhostPositions
        for position in newGhostPositions:
            givenGhostDistance=manhattanDistance(newPos,position)
            if givenGhostDistance < closestGhostDistance:
                closestGhostDistance = givenGhostDistance
        #deincentivize only if ghost is within two moves
        if closestGhostDistance < 3:
            bonus -= 100
        shortestDistance = currentGameState.getWalls().height + currentGameState.getWalls().width # MAX
        farthestDistance = 0 #MIN
        nearestFood = None
        farthestFood = None
        #for loop finds the nearest distance to food
        for food in newFood.asList():
        #print food
            givenDistance = manhattanDistance(newPos, food)
        #print givenDistance
            if givenDistance < shortestDistance:
                shortestDistance = givenDistance
                nearestFood = food
            if givenDistance > farthestDistance:
                farthestDistance = givenDistance
                farthestFood = food
        #incentivize the eating of a food pellet
        if (newFood.asList() < currentGameState.getFood().asList()):
            bonus = 100
        #print successorGameState.getScore()-shortestDistance + bonus        

        #Pacman is currently incentivized to go for the nearest food and eat it unless it is close to a ghost
        return successorGameState.getScore()-shortestDistance + bonus

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        action = minimax(self,gameState,self.depth,0)
        return action
            
        #util.raiseNotDefined()

def minimax(self, gameState, depth, agentIndex):
    #pacman's turn
    numAgents = gameState.getNumAgents()
    #resets to pacman's turn after a number of ghost turns
    if agentIndex%numAgents is 0:
        agentIndex = 0

    if agentIndex is 0:
        pacActions = gameState.getLegalActions(0)
        #returns evaluation at depth limit or leaves
        if len(pacActions) is 0:
            return self.evaluationFunction(gameState)
        if depth is 0:
            return self.evaluationFunction(gameState)
        else:
            children = [gameState.generateSuccessor(0,action) for action in pacActions]    
            values = [minimax(self,child,depth,1) for child in children]
        Max = max(values)
        #returns an action from initial node, value from anywhere else
        if depth is self.depth:
            return pacActions[values.index(Max)]
        else:
            return Max

    #ghosts' turns
    else:
        ghostActions = gameState.getLegalActions(agentIndex)
        #return for leaves
        if len(ghostActions) is 0:
            return self.evaluationFunction(gameState)
        ghostChildren = [gameState.generateSuccessor(agentIndex,action) for action in ghostActions]
        #checks if next turn should be pacman's and decrements depth accordingly
        if agentIndex is numAgents-1:
            depth = depth-1
        ghostValues = [minimax(self,child,depth,agentIndex+1) for child in ghostChildren]
        Min = min(ghostValues)
        return Min
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action = alphabeta(self,gameState,self.depth,0,-sys.maxsize-1,sys.maxsize)
        return action
        util.raiseNotDefined()

def alphabeta(self,gameState,depth,agentIndex,alpha,beta):
#pacman's turn
    numAgents = gameState.getNumAgents()
    #resets to pacman's turn after a number of ghost turns
    if agentIndex%numAgents is 0:
        agentIndex = 0

    if agentIndex is 0:
        pacActions = gameState.getLegalActions(0)
        #returns evaluation at depth limit or leaves
        if len(pacActions) is 0:
            return self.evaluationFunction(gameState)
        if depth is 0:
            return self.evaluationFunction(gameState)
        else:
            Max = -sys.maxsize-1
            t = 0
            for action in pacActions:
                child = gameState.generateSuccessor(0,action)
                tmp = max(Max,alphabeta(self,child,depth,1,alpha,beta))
                if tmp is not Max:
                    Max = tmp
                    t = pacActions.index(action)
                alpha = max(alpha,Max)
                if beta < alpha:
                    break;
        #returns an action from initial node, value from anywhere else
        if depth is self.depth:
            return pacActions[t]
        else:
            return Max

    #ghosts' turns
    else:
        ghostActions = gameState.getLegalActions(agentIndex)
        #return for leaves
        if len(ghostActions) is 0:
            return self.evaluationFunction(gameState)
        #checks if next turn should be pacman's and decrements depth accordingly
        if agentIndex is numAgents-1:
            depth = depth-1
        Min = sys.maxsize
        for action in ghostActions:
            child = gameState.generateSuccessor(agentIndex,action)
            Min = min(Min,alphabeta(self,child,depth,agentIndex+1,alpha,beta))
            beta = min(Min,beta)
            if alpha > beta:
                break
        return Min

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return expectimax(self,gameState,self.depth,0)
        util.raiseNotDefined()

def expectimax(self, gameState, depth, agentIndex):
    #pacman's turn
    numAgents = gameState.getNumAgents()
    #resets to pacman's turn after a number of ghost turns
    if agentIndex%numAgents is 0:
        agentIndex = 0

    if agentIndex is 0:
        pacActions = gameState.getLegalActions(0)
        #returns evaluation at depth limit or leaves
        if len(pacActions) is 0:
            return self.evaluationFunction(gameState)
        if depth is 0:
            return self.evaluationFunction(gameState)
        else:
            children = [gameState.generateSuccessor(0,action) for action in pacActions]    
            values = [expectimax(self,child,depth,1) for child in children]
        Max = max(values)
        #returns an action from initial node, value from anywhere else
        if depth is self.depth:
            return pacActions[values.index(Max)]
        else:
            return Max

    #ghosts' turns
    else:
        ghostActions = gameState.getLegalActions(agentIndex)
        #return for leaves
        if len(ghostActions) is 0:
            return self.evaluationFunction(gameState)
        ghostChildren = [gameState.generateSuccessor(agentIndex,action) for action in ghostActions]
        #checks if next turn should be pacman's and decrements depth accordingly
        if agentIndex is numAgents-1:
            depth = depth-1
        ghostValues = [expectimax(self,child,depth,agentIndex+1) for child in ghostChildren]
        Avg = sum(ghostValues)/len(ghostValues)
        return Avg

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    pacPos = currentGameState.getPacmanPosition()
    feed = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    bonus = 0
    ghostPositions = [ghostState.getPosition() for ghostState in ghostStates]
    closestGhostDistance = currentGameState.getWalls().height + currentGameState.getWalls().width # MAX
    #print newGhostPositions
    for position in ghostPositions:
        givenGhostDistance=manhattanDistance(pacPos,position)
        if givenGhostDistance < closestGhostDistance:
            closestGhostDistance = givenGhostDistance
        #deincentivize only if ghost is within two moves
    if closestGhostDistance < 3:
            bonus -= 100
    shortestDistance = currentGameState.getWalls().height + currentGameState.getWalls().width # MAX
    farthestDistance = 0 #MIN
    nearestFood = None
    farthestFood = None
    #for loop finds the nearest distance to food
    for food in feed.asList():
        #print food
            givenDistance = manhattanDistance(pacPos, food)
        #print givenDistance
            if givenDistance < shortestDistance:
                shortestDistance = givenDistance
                nearestFood = food
            if givenDistance > farthestDistance:
                farthestDistance = givenDistance
                farthestFood = food
    #should incentivize eating food somehow
    
        #print successorGameState.getScore()-shortestDistance + bonus        

        #Pacman is currently incentivized to go for the nearest food and eat it unless it is close to a ghost
    return currentGameState.getScore()

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

