# Импорт библиотек
from fastapi import FastAPI
# Импорт функции из файла \TST\summary_text\src\router.py
from TST.summary_text.src.router import router as router_summary_text

app = FastAPI(
    title="Common api"
)

app.include_router(router_summary_text)
