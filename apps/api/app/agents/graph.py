from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.supervisor import SupervisorAgent
from app.agents.nodes.accountant import AccountantAgent
from app.agents.nodes.cfo import CFOAgent
from app.agents.nodes.auditor import AuditorAgent


supervisor = SupervisorAgent()
accountant = AccountantAgent()
cfo = CFOAgent()
auditor = AuditorAgent()


def route(state: AgentState):
    return supervisor.route(state["message"])


def accountant_node(state: AgentState):
    result = accountant.run(
        state["message"],
        state["organization_id"],
        db=state.get("db"),
    )
    return {"response": result}


def cfo_node(state: AgentState):
    result = cfo.run(
        state["message"],
        state["organization_id"],
        db=state.get("db"),
    )
    return {"response": result}


def auditor_node(state: AgentState):
    result = auditor.run(
        state["message"],
        state["organization_id"],
        db=state.get("db"),
    )
    return {"response": result}


graph = StateGraph(AgentState)

graph.add_node("accountant", accountant_node)
graph.add_node("cfo", cfo_node)
graph.add_node("auditor", auditor_node)

graph.set_conditional_entry_point(
    route,
    {
        "ACCOUNTANT": "accountant",
        "CFO": "cfo",
        "AUDITOR": "auditor",
    },
)

graph.add_edge("accountant", END)
graph.add_edge("cfo", END)
graph.add_edge("auditor", END)

app_graph = graph.compile()