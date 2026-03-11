class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        self.tools[name] = func

    def get(self, name):
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not registered")

        return self.tools[name]