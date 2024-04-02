import random
from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        foodStates = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        # print(f"the current action is {action}")
        # print(f"{newScaredTimes}")
        oldFood = foodStates.asList()
        # We need to get the positions of the ghosts such that pacman doesn't
        # get eaten accidentally.
        x1, y1 = newPosition
        ghostIndex = 0
        for gp in successorGameState.getGhostPositions():
            if newScaredTimes[ghostIndex] == 0:
                gx, gy = gp
                gdx = x1 - gx
                gdy = y1 - gy
                if abs(gdx) + abs(gdy) < 3:
                    # print(f"THE GHOST IS VERY CLOSE TO PACMAN!!
                    if abs(gdx) < abs(gdy):
                        # print("action is less than action")
                        if action == "West" and gdx < 0:
                            # print("the best action is to move West")
                            # If the ghost is to the right of pacman.
                            return successorGameState.getScore() + 20
                        elif action == "East" and gdx > 0:
                            # print("the best action is to move East")
                            return successorGameState.getScore() + 20
                    if abs(gdx) > abs(gdy):
                        if action == "North" and gdy > 0:
                            # print("the best action is to move North")
                            return successorGameState.getScore() + 20
                        elif action == "South" and gdy < 0:
                            # print("the best action is to move South")
                            return successorGameState.getScore() + 20
                    return successorGameState.getScore() - 20
        for scaredTimes in newScaredTimes:
            if scaredTimes > 0:
                for gp in successorGameState.getGhostPositions():
                    if gp == newPosition:
                        return successorGameState.getScore() + 200
        distToFood = []
        for eachFood in oldFood:
            x, y = eachFood
            x2 = x1 - x
            if x2 < 0:
                # if the food is to the right of the pacman.
                x2 *= -1
            y2 = y1 - y
            if y2 < 0:
                # if the food is above the pacman.
                y2 *= -1
            distToFood.append(((y2 + x2), x1, y1))
        min = 99999
        for dist in distToFood:
            if dist[0] < min:
                min = dist[0]
        if min == 0:
            return successorGameState.getScore() + 1
        return successorGameState.getScore() + 1 / min
        """xDist = x1 - dist[1]
        yDist = y1 - dist[2]
        if (abs(xDist) < abs(yDist)):
            if action == "West":
                if xDist > 0:
                    return successorGameState.getScore() + abs(xDist)
            elif action == "East":
                if yDist < 0:
                    return successorGameState.getScore() + abs(xDist)
        if (abs(xDist) > abs(yDist)):
            if action == "South":
                if yDist > 0:
                    return successorGameState.getScore() + abs(yDist)
            elif action == "North":
                if yDist < 0:
                    return successorGameState.getScore() + abs(yDist)
        return successorGameState.getScore()"""
        

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.
    THIS IS THE SYNTAX FOR THIS METHOD: generateSuccessor(agent index, cardinal action)

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    # Should work for any number of ghosts. The minimax tree will have multiple min layers for
    # every max layer.
    # A single search would mean pacman and the all the ghosts moving one time.
    # Min and Max need to return scores with their moves.
    # getEvaluationFunction() takes in a state.

    # we need depth, turn (whose turn is it), state.

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def max_agent(self, agent_index, gameState, depth):
        # we have to check in if we are in the terminal state. If the max tree depth reached,
        # terminate. IF is win or is lose, then terminate.
        max_value = -float('inf')
        max_move = "Stop"
        # print(f"the agent index is {depth % (gameState.getNumAgents()-1)} FOR THE max FUNCTION")
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.getEvaluationFunction()(gameState), None
        for each_action in actions:
            successorState = gameState.generateSuccessor(agent_index, each_action)
            value, move = self.value(agent_index + 1, successorState, depth)
            if value > max_value:
                max_value = value
                max_move = each_action
        return max_value, max_move
    
    def min_agent(self, agent_index, gameState, depth):
        min_value = float('inf')
        min_move = "Stop"
        # We need to get the legal actions such that pacman and ghosts will take
        # the best of the 4 actions possible, if legal
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.getEvaluationFunction()(gameState), None
        for each_action in actions:
            successorState = gameState.generateSuccessor(agent_index, each_action)
            value, move = self.value(agent_index + 1, successorState, depth)
            if value < min_value:
                min_value = value
                min_move = each_action
        return min_value, min_move
    
    def value(self, agent_index, gameState, depth):
        if agent_index >= gameState.getNumAgents():
            depth += 1
        if agent_index >= gameState.getNumAgents() and depth >= self.getTreeDepth():
            print(f"terminal State returned is {self.getEvaluationFunction()(gameState)}")
            return self.getEvaluationFunction()(gameState), None
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
            depth += 1
        if agent_index == 0:
            value, move = self.max_agent(agent_index, gameState, depth)
            return value, move
        if agent_index != 0:
            value, move = self.min_agent(agent_index, gameState, depth)
            return value, move

    def getAction(self, gameState):
        value, move = self.value(0, gameState, 0)
        return move

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def max_agent(self, agent_index, gameState, depth, alpha, beta):
        # we have to check in if we are in the terminal state. If the max tree depth reached,
        # terminate. IF is win or is lose, then terminate.
        max_value = -float('inf')
        max_move = "Stop"
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.getEvaluationFunction()(gameState), None
        print(f"the legal actions for agent {agent_index} are {actions}")
        for each_action in actions:
            print(f"action for agent {agent_index} is {each_action}")
            successorState = gameState.generateSuccessor(agent_index, each_action)
            
            value, move = self.value(agent_index + 1, successorState, depth, alpha, beta)
            if value > max_value:
                max_value = value
                max_move = each_action
                alpha = max(alpha, max_value)
            if max_value >= beta:
                return max_value, max_move
        return max_value, max_move
    
    def min_agent(self, agent_index, gameState, depth, alpha, beta):
        min_value = float('inf')
        min_move = "Stop"
        # We need to get the legal actions such that pacman and ghosts will take the best of the
        # 4 actions possible, if legal
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.getEvaluationFunction()(gameState), None
        print(f"the legal actions for agent {agent_index} are {actions}")
        for each_action in actions:
            print(f"action for agent {agent_index} is {each_action}")
            successorState = gameState.generateSuccessor(agent_index, each_action)
            print(f"value called with {agent_index + 1} with depth of {depth}")
            value, move = self.value(agent_index + 1, successorState, depth, alpha, beta)
            if value < min_value:
                min_value = value
                min_move = each_action
                beta = min(beta, min_value)
            if min_value <= alpha:
                return min_value, move
        return min_value, min_move

    def value(self, agent_index, gameState, depth, alpha, beta):
        # print(f"value has been caled with agent {agent_index} and depth {depth}")
        if agent_index >= gameState.getNumAgents():
            depth += 1
        if agent_index >= gameState.getNumAgents() and depth >= self.getTreeDepth():
            print(f"terminal State returned is {self.getEvaluationFunction()(gameState)}")
            return self.getEvaluationFunction()(gameState), None
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
        if agent_index == 0:
            value, move = self.max_agent(agent_index, gameState, depth, alpha, beta)
            return value, move
        if agent_index != 0:
            value, move = self.min_agent(agent_index, gameState, depth, alpha, beta)
            return value, move

    def getAction(self, gameState):
        alpha = -float('inf')
        beta = float('inf')
        value, move = self.value(0, gameState, 0, alpha, beta)
        print(f"the move to be returned is {move} with a score of {value}.")
        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """
    
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def expectation(self, gameState, agent_index, depth):
        min_move = "exp"
        # rint(f"the agent index is {depth % (gameState.getNumAgents()-1)} FOR THE MIN FUNCTION")
        # We need to get the legal actions such that pacman and ghosts will take the best of the
        # 4 actions possible, if legal
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.getEvaluationFunction()(gameState), None
        values = 0
        for each_action in actions:
            successorState = gameState.generateSuccessor(agent_index, each_action)
            eval, move = self.value(successorState, agent_index + 1, depth)
            values += eval * float(1 / len(actions))
        return values, min_move

    def max_agent(self, gameState, agent_index, depth):
        # we have to check in if we are in the terminal state. If the max tree depth reached,
        # terminate. IF is win or is lose, then terminate.
        max_value = -float('inf')
        max_move = "Stop"
        # print(f"the agent index is {agent_index} FOR THE max FUNCTION")
        actions = gameState.getLegalActions(agent_index)
        # print(f"pacman legal actions include {actions}")
        for each_action in actions:
            print(f"{each_action}")
            successorState = gameState.generateSuccessor(agent_index, each_action)
            value, move = self.value(successorState, agent_index + 1, depth)
            if value > max_value:
                max_value = value
                max_move = each_action
        return max_value, max_move

    def value(self, gameState, agent_index, depth):
        
        if depth >= self.getTreeDepth() and agent_index >= gameState.getNumAgents():
            # print(f"{self.getEvaluationFunction()(gameState)} returned")
            return self.getEvaluationFunction()(gameState), None
        if agent_index >= gameState.getNumAgents():
            depth += 1
            agent_index = 0
        if agent_index == 0:
            value, move = self.max_agent(gameState, 0, depth)
            return value, move
        if agent_index != 0:
            value, move = self.expectation(gameState, agent_index, depth)
            return value, move
    
    def getAction(self, gameState):
        # print("GET ACTION CALLED!!!")
        value, move = self.value(gameState, 0, 1)
        # print(f"the value and move being return is {value}, {move}")
        return move
    
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    # We want to calculate the distance to the closeest food and give a reward for that direction.
    # We also want to calualte the distance to the closest ghosts, if its scared give it a
    # reward for nearing it.

    x, y = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    if len(foodPositions) == 0:
        return currentGameState.getScore()
    min_food_position = (foodPositions[0])
    min_food_dist = abs(min_food_position[0] - x) + abs(min_food_position[1] - y)
    for food in foodPositions:
        dx = abs(food[0] - x)
        dy = abs(food[1] - y)
        foodDist = dx + dy
        mx, my = min_food_position
        mdx = abs(mx - x)
        mdy = abs(my - y)
        min_food_dist = mdx + mdy
        if min_food_dist > foodDist:
            min_food_position = food
    return currentGameState.getScore() + (1 / min_food_dist)

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
