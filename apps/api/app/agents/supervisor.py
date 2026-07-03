from app.agents.providers import GeminiProvider
from app.agents.prompts import SUPERVISOR_PROMPT


class SupervisorAgent:
    """
    Routes user query to correct specialist agent:
    CFO / ACCOUNTANT / AUDITOR
    """

    def __init__(self):
        self.llm = GeminiProvider()

    def route(self, message: str) -> str:
        """
        Returns:
            "CFO" | "ACCOUNTANT" | "AUDITOR"
        """

        response = self.llm.chat(
            message=message,
            system_prompt=SUPERVISOR_PROMPT,
        )

        decision = response.strip().upper()

        # safety fallback
        if "CFO" in decision:
            return "CFO"
        if "ACCOUNTANT" in decision:
            return "ACCOUNTANT"
        if "AUDITOR" in decision:
            return "AUDITOR"

        # default fallback
        return "ACCOUNTANT"