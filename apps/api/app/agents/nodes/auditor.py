from app.agents.registry import TOOLS
from app.agents.providers import GeminiProvider
from app.agents.prompts import AUDITOR_PROMPT


class AuditorAgent:
    """
    Detects:
    - anomalies
    - inconsistencies
    - missing invoices/payments
    """

    def __init__(self):
        self.llm = GeminiProvider()

    def run(self, message: str, organization_id: int, db) -> str:
        prompt = f"""
{AUDITOR_PROMPT}

User Request:
{message}

Available tools:
- unpaid_invoices
- invoice_count
- payment_count

Return ONLY tool name.
"""

        tool_name = self.llm.chat(prompt).strip().lower()

        tool = TOOLS.get(tool_name)

        if not tool:
            tool_name = "unpaid_invoices"
            tool = TOOLS[tool_name]

        result = tool(db=db, organization_id=organization_id)

        final_prompt = f"""
You are an Auditor Agent.

User asked: {message}

Tool used: {tool_name}

Result: {result}

Explain anomalies clearly.
"""

        return self.llm.chat(final_prompt)