from planner import Planner
from memory import Memory
from security.schema_validator import validate_action
from security.authorization import AuthorizationManager


class SafeAgent:

    def __init__(self, role, router):

        self.role = role
        self.router = router
        self.auth = AuthorizationManager()

        self.planner = Planner()
        self.memory = Memory()

    def run(self, user_input):

        for step in range(5):  # max steps

            action_dict = self.planner.plan(
                user_input,
                self.memory.get_history()
            )

            action = validate_action(action_dict)

            self.auth.authorize(self.role, action.tool)

            result = self.router.route(action)

            self.memory.add(action_dict, result)

            if action.tool == "final_answer":
                return result