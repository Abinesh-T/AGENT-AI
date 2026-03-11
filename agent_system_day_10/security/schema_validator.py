from models.action_schema import AgentAction
from pydantic import ValidationError


def validate_action(action_dict):

    try:
        action = AgentAction(**action_dict)
        return action

    except ValidationError as e:
        raise ValueError(f"Invalid action schema: {e}")