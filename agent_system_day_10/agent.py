from security.schema_validator import validate_action
from security.authorization import AuthorizationManager
from tools.router import ToolRouter


class SafeAgent:

    def __init__(self, role, router):

        self.role = role
        self.router = router
        self.auth = AuthorizationManager()

    def execute(self, action_dict):

        # 1 validate schema
        action = validate_action(action_dict)

        # 2 authorization
        self.auth.authorize(self.role, action.tool)

        # 3 route tool
        result = self.router.route(action)

        return result