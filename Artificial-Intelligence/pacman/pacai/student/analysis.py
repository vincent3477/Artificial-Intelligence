"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    I gave a large penalty for living because the agent wants the closest
    exit possible and the fastest path to get there.
    """

    answerDiscount = 0.1
    answerNoise = 0.011
    answerLivingReward = -5

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    I changed the discount to be lower because the agent wants the soonest exit
    possible. I also gave it a reward to incentivize the agent to stay longer.
    """

    answerDiscount = 0.35
    answerNoise = 0.2
    answerLivingReward = 0.02

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    I gave a negative living reward, but gave a high discount rate.
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = -0.9

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]
    Left values unaltered.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    I gave very high noise factors, such that the agent is more likely to take unexpected actions.
    """

    answerDiscount = 0.0
    answerNoise = 0.8
    answerLivingReward = 0.9

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    wrong
    """

    # answerEpsilon = 0.3
    # answerLearningRate = 0.5

    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
