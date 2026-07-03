from app.agents.registry import TOOLS
from app.agents.providers import GeminiProvider
from app.agents.prompts import CFO_PROMPT


class CFOAgent:
    """
    Handles:
    - Revenue
    - Business summary
    - Outstanding
    - Financial overview
    """

    def __init__(self):
        self.llm = GeminiProvider()

    def run(self, message: str, organization_id: int, db) -> str:
        prompt = f"""
{CFO_PROMPT}

User Request:
{message}

Available tools:
- business_summary
- revenue
- payment_total
- outstanding
- unpaid_invoices
- customer_count
- invoice_count

Return ONLY tool name or "business_summary".
"""

        tool_name = self.llm.chat(prompt).strip().lower()

        tool = TOOLS.get(tool_name)

        if not tool:
            tool_name = "business_summary"
            tool = TOOLS[tool_name]

        result = tool(db=db, organization_id=organization_id)

        final_prompt = f"""
You are CFO Agent.

User asked: {message}

Tool: {tool_name}

Result: {result}

Explain like a CFO in simple business language.
"""

        return self.llm.chat(final_prompt)