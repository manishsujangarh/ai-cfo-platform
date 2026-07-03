from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def chat(
        self,
        message: str,
    ) -> str:
        pass