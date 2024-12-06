import numpy as np


class DecisionAgent:
    def __init__(self, strategy="random"):
        self.strategy = strategy

    def decide(self, opponent_action=None):
        if self.strategy == "random":
            return "cooperate" if np.random.rand() > 0.5 else "defect"
        elif self.strategy == "tit_for_tat":
            return opponent_action if opponent_action else "cooperate"
        else:
            raise ValueError("Unknown strategy!")
