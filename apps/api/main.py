from fastapi import FastAPI

app = FastAPI(
    title="AI CFO API",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "AI CFO API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}