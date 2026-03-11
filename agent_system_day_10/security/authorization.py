class AuthorizationManager:

    def __init__(self):

        self.permissions = {
            "calculator": ["math_agent", "general_agent"],
            "web_search": ["research_agent", "general_agent"]
        }

    def authorize(self, agent_role, tool_name):

        allowed_roles = self.permissions.get(tool_name, [])

        if agent_role not in allowed_roles:
            raise PermissionError(
                f"Agent role '{agent_role}' not allowed to use '{tool_name}'"
            )

        return True