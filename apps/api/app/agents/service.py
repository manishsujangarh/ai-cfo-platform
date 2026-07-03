from app.agents.graph import app_graph


class AgentService:
    def run(self, message: str, organization_id: int, user_id: int, db):
        result = app_graph.invoke(
            {
                "message": message,
                "organization_id": organization_id,
                "user_id": user_id,
                "db": db,
            }
        )

        return result["response"]