from app.agents.providers import GeminiProvider

provider = GeminiProvider()

print(
    provider.chat(
        "Say hello in one sentence."
    )
)