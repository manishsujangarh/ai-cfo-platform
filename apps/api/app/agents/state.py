from typing import TypedDict, Optional, Any


class AgentState(TypedDict):
    # user input
    message: str

    # routing
    next_agent: Optional[str]

    # conversation context
    response: Optional[str]

    # tool execution
    tool_name: Optional[str]
    tool_args: Optional[dict]
    tool_result: Optional[Any]

    # metadata
    organization_id: int
    user_id: int