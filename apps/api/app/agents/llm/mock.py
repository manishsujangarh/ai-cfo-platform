from app.agents.llm.base import BaseLLM


class MockLLM(BaseLLM):

    def chat(
        self,
        message: str,
    ) -> str:
        return message.lower()