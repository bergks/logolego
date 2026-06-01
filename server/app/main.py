from fastapi import FastAPI
from app.routers import cards, tasks

app = FastAPI()

app.include_router(cards.router)
app.include_router(tasks.router)

@app.get('/health')
def health_check():
    return {'health': 'ok'}