from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.
        self.states = mdp.getStates()  # get all the valid states.
        self.Qvalues = {}

        # Compute the values here.

        iterations = 1
        
        while (iterations <= iters):
            for state in self.states:
                actions = mdp.getPossibleActions(state)
                for action in actions:
                    next_states = mdp.getTransitionStatesAndProbs(state, action)
                    print(f"\n\nour next states for state {state} is {next_states}")
                    Q_reward_val = 0
                    for ns in next_states:
                        transition_probability = ns[1]
                        transition_state = ns[0]
                        Q_reward_val1 = transition_probability * \
                            (self.mdp.getReward(state, action, transition_state)
                            + (self.discountRate * self.values.get(transition_state, 0.0)))
                        Q_reward_val += Q_reward_val1
                        print(f"for state {state} the action is {action}")
                        print(f"transition probility is {transition_probability}")
                        print(f"reward is {mdp.getReward(state, action, transition_state)}")
                        print(f"transition probility is {transition_probability}")
                        print(f"next state {transition_state}")
                        print(f"our qv to be added is {Q_reward_val1}")
                    print(f"our qv is therefore {Q_reward_val}")
                    self.Qvalues[(state, action)] = Q_reward_val
                    """if not (mdp.isTerminal(next_states[0][0])):
                        # print(f"state {next_states[0]} is not a terminal state!")
                        max_q = -99999
                        for a in actions:
                            if self.Qvalues.get((state, a), -99999) > max_q:
                                max_q = self.Qvalues.get((state, a), -99999)
                        self.values[state] = max_q
                    elseQ
                        self.values[state] = Q_reward_val"""
            for state in self.states:
                actions1 = mdp.getPossibleActions(state)
                max_q = 0
                if len(actions1) != 0:
                    max_q = self.Qvalues[(state, actions1[0])]
                for action in actions1:
                    if self.Qvalues[(state, action)] > max_q:
                        max_q = self.Qvalues[(state, action)]
                self.values[state] = max_q
            iterations += 1
        print(self.Qvalues)

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
    
    def get_adj_state(self, state, action):
        if action == 'exit':
            return 'TERMINAL_STATE'
        if action == 'west':
            return (state[0] - 1, state[1])
        if action == 'east':
            return (state[0] + 1, state[1])
        if action == 'north':
            return (state[0], state[1] + 1)
        if action == 'west':
            return (state[0], state[1] - 1)
    
    def getPolicy(self, state):
        """action_value_pair = {}
        actions = self.mdp.getPossibleActions(state)
        max_action = None
        if len(actions) == 0:
            return None

        for action in actions:
            if action == 'exit':
                return 'exit'
            adj_state = self.get_adj_state(state, action)
            if adj_state in self.states:
                max_action = action
                action_value_pair[action] = self.values.get(adj_state)
            

        print(f"our current state is {state}")
        for move in action_value_pair.keys():
            if action_value_pair.get(move) > action_value_pair.get(max_action):
                max_action = move
        print(f"the max action is returning {max_action} for state {state}")
        return max_action"""
        """print(f"mdp states are {self.mdp.getStates()}")
        actions = self.mdp.getPossibleActions(state)
        action_value_pair = {}
        if len(actions) == 0:
            return None
        for a in actions:
            next_states = self.mdp.getTransitionStatesAndProbs(state, a)
            max_value = -99999
            for ns in next_states:
                value_state = self.values.get(ns[0])
                if value_state != None and value_state > max_value:
                    max_value = value_state
            action_value_pair[a] = max_value
        max_action = actions[0]
        print(action_value_pair)
        for an_action in action_value_pair.keys():
            if action_value_pair.get(an_action) > action_value_pair.get(max_action):
                max_action = an_action
        return max_action
        """
        
        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None
        if actions[0] == 'exit':
            return 'exit'
        max_action = actions[0]
        for a in actions:
            if round(self.getQValue(state, a), 2) > round(self.getQValue(state, max_action), 2):
                max_action = a
        actions_with_ties = []
        for a in actions:
            if max_action != a:
                if self.getQValue(state, a) == self.getQValue(state, max_action):
                    actions_with_ties.append(a)
        if len(actions_with_ties) == 0:
            return max_action
        actions_with_ties.append(max_action)
        max_adjacent_value = -99999
        max_move = max_action
        for awt in actions_with_ties:
            ns = self.get_adj_state(state, awt)
            if ns in self.mdp.getStates():
                ns_val = self.values.get(ns)
                if ns_val > max_adjacent_value:
                    max_adjacent_value = ns_val
                    max_move = awt
        return max_move
    
    def getQValue(self, state, action):
        return self.Qvalues.get((state, action))
