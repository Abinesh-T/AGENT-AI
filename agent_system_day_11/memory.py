class Memory:

    def __init__(self):
        self.steps = []

    def add(self, action, observation):

        self.steps.append({
            "action": action,
            "observation": observation
        })

    def get_history(self):
        return self.steps