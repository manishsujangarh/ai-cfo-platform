from fastapi import FastAPI

app = FastAPI(
    title="AI CFO API",
    description="Production AI CFO Platform",
    version="0.1.0",
)

@app.get("/api/v1")
def root():
    return {
        "message": "Welcome to AI CFO API v1"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }