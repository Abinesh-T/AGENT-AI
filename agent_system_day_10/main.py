from agent import SafeAgent
from tools.registry import ToolRegistry
from tools.router import ToolRouter
from tools.calculator import calculator


registry = ToolRegistry()
registry.register("calculator", calculator)

router = ToolRouter(registry)

agent = SafeAgent(
    role="math_agent",
    router=router
)


action = {
    "tool": "calculator",
    "parameters": {
        "expression": "5 * 8"
    }
}


result = agent.execute(action)

print(result)