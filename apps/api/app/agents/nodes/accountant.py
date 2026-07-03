from app.agents.registry import TOOLS
from app.agents.providers import GeminiProvider
from app.agents.prompts import ACCOUNTANT_PROMPT


class AccountantAgent:
    """
    Handles:
    - Customers
    - Vendors
    - Invoices
    - Payments
    """

    def __init__(self):
        self.llm = GeminiProvider()

    def run(self, message: str, organization_id: int, db) -> str:
        """
        Step 1: Decide tool
        Step 2: Execute tool
        Step 3: Return response
        """

        prompt = f"""
{ACCOUNTANT_PROMPT}

User Request:
{message}

Available tools:
- customer_count
- vendor_count
- invoice_count
- payment_count
- payment_total
- unpaid_invoices

Return ONLY the tool name to use.
"""

        tool_name = self.llm.chat(message=prompt).strip().lower()

        tool = TOOLS.get(tool_name)

        if not tool:
            return "I could not determine the correct accounting tool."

        # execute tool
        result = tool(db=db, organization_id=organization_id)

        # final response
        final_prompt = f"""
You are an Accountant Agent.

User asked: {message}

Tool used: {tool_name}

Result: {result}

Return a clear financial answer.
"""

        return self.llm.chat(final_prompt)