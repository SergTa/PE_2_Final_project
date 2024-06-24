from fastapi import FastAPI

from src.router import router as router_summary_text

app = FastAPI(
    title="Common api"
)

app.include_router(router_summary_text)
