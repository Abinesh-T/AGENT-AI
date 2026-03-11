from agent import SafeAgent
from tools.registry import ToolRegistry
from tools.router import ToolRouter
from tools.calculator import calculator
from tools.final_answer import final_answer


registry = ToolRegistry()
registry.register("calculator", calculator)
registry.register("final_answer", final_answer)

router = ToolRouter(registry)

agent = SafeAgent(
    role="math_agent",
    router=router
)


result = agent.run("What is 15 * 9?")

print(result)