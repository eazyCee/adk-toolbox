import os
import dotenv
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.callback_context import CallbackContext
from .tools import toolset

# Load environment variables
dotenv.load_dotenv()

async def init_state(ctx: CallbackContext) -> None:
    """Initialize default state variables before the agent runs."""
    if "company" not in ctx.state:
        ctx.state["company"] = "ESB"

prompt_template = """
    You are a helpful product listing optimizer. You can help users search for products using semantic search and optimize product listings by suggesting and updating product attributes.
    When a user asks about adding attributes to increase sales, analyze the product (e.g. if it is a wine, recommend country of origin, type of grape, etc.) and offer to update the attributes for them.
    Use the provided tools to execute these actions. The current company is {company}.
"""

root_agent = Agent(
    model='gemini-2.0-flash',
    name='sales_analytics_agent',
    description='A sales analytics and product listing optimizer assistant',
    instruction=prompt_template,
    tools=toolset,
    before_agent_callback=init_state
)

a2a_app = to_a2a(root_agent, port=int(os.environ.get('A2A_PORT', 8001)))
