from app.agents.registry import Tool, registry

registry.register(
    Tool(
        name="customer_count",
        description="Return the total number of customers.",
        function=get_customer_count,
    )
)