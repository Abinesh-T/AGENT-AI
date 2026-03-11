import json
import re

from get_client import client


def _extract_json(raw: str) -> str:
    """Strip markdown code fences if present."""
    raw = (raw or "").strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
    if match:
        return match.group(1).strip()
    return raw


class Planner:

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def plan(self, user_input, history):

        prompt = f"""
                    You are an AI agent.

                    Available tools:
                    - calculator(expression)

                    Return ONLY JSON without any markdown code fences:

                    Example:
                    {{
                    "tool": "calculator",
                    "parameters": {{
                        "expression": "2+2"
                    }}
                    }}

                    User request:
                    {user_input}
                """

        response = client.models.generate_content(
            model=self.model,
            contents=[
                prompt,
                user_input
            ]
        )
        try:
            raw = response.text
        except (ValueError, AttributeError):
            raw = ""
        raw = _extract_json(raw or "")
        if not raw:
            raise ValueError(
                "Planner got no text from model (empty or blocked). Check API key and model."
            )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Planner model did not return valid JSON: {e}. Raw (first 200 chars): {raw[:200]!r}"
            ) from e