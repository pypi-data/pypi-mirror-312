class Environment:
    def __init__(self, agents):
        self.agents = agents

    def run(self, rounds=10):
        for _ in range(rounds):
            actions = [agent.decide() for agent in self.agents]
            print(f"Round actions: {actions}")
