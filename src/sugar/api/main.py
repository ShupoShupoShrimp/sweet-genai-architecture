from fastapi import FastAPI
from sugar.api.routes import health

app = FastAPI(
    title="Sweet GenAi Architecture",
    description="Production-grade GenAI platform providing grounded RAG, graph context, multi-agent orchestration, and LLMOps.",
    version="0.1",
)

app.include_router(health.router)
