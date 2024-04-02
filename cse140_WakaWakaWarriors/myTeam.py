from pacai.agents.capture.capture import CaptureAgent
import random


def createTeam(firstIndex, secondIndex, isRed,
               first='pacai.agents.capture.dummy.DummyAgent',
               second='pacai.agents.capture.dummy.DummyAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = FirstAgent(firstIndex)
    secondAgent = FirstAgent(secondIndex)

    return [
        firstAgent,
        secondAgent,
    ]


class FirstAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

        # Your initialization code goes here, if you need any.

        if self.index != min(self.getTeam(gameState)):
            self.priority = 'bot'
        else:
            self.priority = 'top'

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        actions = gameState.getLegalActions(self.index)
        values = [self.evaluate(gameState, a) for a in actions]

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features[feature] * weights[feature] for feature in features)

        return stateEval

    def getWeights(self, gameState, action):
        """
        Returns a dict of weights for the state.
        The keys match up with the return from `ReflexCaptureAgent.getFeatures`.
        """
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'distanceToThreat': 0,
            'distanceToPacman': -1,
            'rewardEatPacman': 10,
            'distanceToVulGhost': 0,
        }

    def getFeatures(self, gameState, action):
        """
        Returns a dict of features for the state.
        """
        distanceToFood = 0
        # distanceToThreat = 0
        distanceToPacman = 0
        rewardEatPacman = 0
        # distanceToVulGhost = 0

        nextGameState = gameState.generateSuccessor(self.index, action)
        successorScore = self.getScore(nextGameState)

        position = nextGameState.getAgentState(self.index).getPosition()

        food_list = self.getFood(nextGameState).asList()
        # capsule_list = self.getCapsules(nextGameState)
        if self.priority == 'top':
            new_food_list = [i for i in (food_list) if i[1] >= gameState.getWalls().getHeight() / 2]
            if not new_food_list:
                new_food_list = food_list
        else:
            new_food_list = [i for i in (food_list) if i[1] < gameState.getWalls().getHeight() / 2]
            if not new_food_list:
                new_food_list = food_list

        minDistance = None
        for food in new_food_list:
            distance = self.getMazeDistance(position, food)
            if minDistance is None or minDistance > distance:
                minDistance = distance
        if minDistance is not None:
            distanceToFood = minDistance

        opponent_index = self.getOpponents(gameState)
        opps_pos = [gameState.getAgentPosition(i) for i in opponent_index]
        targets = []

        # get eatable pacmen
        if self.red and nextGameState.isOnRedSide(position):
            for i in range(len(opponent_index)):
                if nextGameState.isOnRedSide(opps_pos[i]):
                    targets.append(opps_pos[i])
        elif not self.red and nextGameState.isOnBlueSide(position):
            for i in range(len(opponent_index)):
                if nextGameState.isOnBlueSide(opps_pos[i]):
                    targets.append(opps_pos[i])
        minDistance = None
        for target_pos in targets:
            distance = self.getMazeDistance(position, target_pos)
            if minDistance is None or distance < minDistance:
                minDistance = distance
                if minDistance == 0:
                    rewardEatPacman = 1
                    break
        if targets and minDistance is not None:
            distanceToFood = 0
            distanceToPacman = minDistance

        return {
            'successorScore': successorScore,
            'distanceToFood': distanceToFood,
            'distanceToThreat': 0,
            'distanceToPacman': distanceToPacman,
            # (1 / distanceToPacman) if distanceToPacman else 0,
            'rewardEatPacman': rewardEatPacman,
            'distanceToVulGhost': 0,
        }
