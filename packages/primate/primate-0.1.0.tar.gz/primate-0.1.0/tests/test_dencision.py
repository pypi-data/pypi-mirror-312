import unittest
from primate.decision.agent import DecisionAgent


class TestDecisionAgent(unittest.TestCase):
    def test_random_strategy(self):
        agent = DecisionAgent(strategy="random")
        self.assertIn(agent.decide(), ["cooperate", "defect"])
