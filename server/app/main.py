from fastapi import FastAPI
from app.routers import cards, tasks, modules

app = FastAPI()

app.include_router(cards.router)
app.include_router(tasks.router)
app.include_router(modules.router)

@app.get('/health')
def health_check():
    return {'health': 'ok'}