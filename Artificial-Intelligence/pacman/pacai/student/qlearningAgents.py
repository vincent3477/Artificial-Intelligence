from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util.probability import flipCoin
import random

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.QValues = {}
        # self.reinforcementAgent = ReinforcementAgent()

    def update(self, state, action, nextState, reward):
        sample = 0.0
        if self.getValue(nextState) is None:
            sample = reward
        else:
            sample = reward + self.getDiscountRate() * self.getValue(nextState)
        Qval = 0.0
        if (state, action) in self.QValues:
            Qval = self.QValues.get((state, action))
        self.QValues[(state, action)] = (1 - self.getAlpha()) * Qval + self.getAlpha() * sample

    def getAction(self, state):
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            # print(f"none for state {state} being returned.")
            return None
        if flipCoin(self.getEpsilon()) == 1:
            return random.choice(actions)
        return self.getPolicy(state)

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        if (state, action) not in self.QValues:
            return 0.0
        else:
            return self.QValues.get((state, action))

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0.0
        max_action = -99999999
        for a in actions:
            if max_action < self.getQValue(state, a):
                max_action = self.getQValue(state, a)
        return max_action

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None
        max_action = -999999
        for a in actions:
            if max_action < self.getQValue(state, a):
                max_action = self.getQValue(state, a)
        # print(f"our best action is {max_move}")
        list_actions = []
        for a in actions:
            # print(f"current at ation {a}")
            # print(f"max action is {ma
            # x_action} and Qval we are looking at is {self.getQValue(state, a)}")
            if max_action == self.getQValue(state, a):
                # print(f"add {a}")
                list_actions.append(a)
        return random.choice(list_actions)
        

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # weights is a dictionary of a vector of weights each mapping to features.
        # {features -> weight_values.}
        # feature would be either on or off (0 or 1) in most cases.
        # Q(s,a) would be equal to w1 * f1(s,a) + w2 * f2(s,a) etc .....
        # this is why Q would represent a dot product vector
        # the error would be the the reward - the current Q value estimate.
        # update should update all wi with the error being Reward(state, action) -
        # getQvalue(state, action)

        self.weights = {'bias': 0.0, '#-of-ghosts-1-step-away': 0.0, 'eats-food': 0.0,
                        'closest-food': 0.0}
        # self.Qvalues = {}

    def getQValue(self, state, action):
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)
        q_value = 0.0
        for f in features.keys():
            # if self.weights.get(f) != None:
            q_value += self.weights.get(f) * features.get(f)
        # print(f"q value being returned for {action} is {q_value}")
        # print(f"the weights are {self.weights}")
        return q_value

    def update(self, state, action, nextState, reward):
        # need to update each weight_i based on feature_i
        features = self.featExtractor.getFeatures(self.featExtractor, state, action)
        for f in features.keys():
            if f == '#-of-ghosts-1-step-away' and features.get(f) != 0.0:
                print(f"current inspecting feature {f}")
                print(f"the value for that feature is {features.get(f)}\n\n")
            w = self.weights.get(f)
            error = (reward + (self.getGamma() * self.getValue(nextState))) \
                - self.getQValue(state, action)
            self.weights[f] = w + self.getAlpha() * error * features.get(f)
            # if w != None:
            #     self.weights[f] = w + self.getAlpha() * error * features.get(f)
            # else:
            #     self.weights[f] = self.getAlpha() * error * features.get(f)

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            print(self.weights)
