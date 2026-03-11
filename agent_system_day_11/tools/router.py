class ToolRouter:

    def __init__(self, registry):
        self.registry = registry

    def route(self, action):

        tool_function = self.registry.get(action.tool)

        return tool_function(**action.parameters)