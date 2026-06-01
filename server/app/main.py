from fastapi import FastAPI
from app.routers import cards, tasks, modules, pupils, auth
from app.routers.homework import logoped_router, public_router

app = FastAPI()

app.include_router(auth.router)
app.include_router(cards.router)
app.include_router(tasks.router)
app.include_router(modules.router)
app.include_router(pupils.router)
app.include_router(logoped_router)
app.include_router(public_router)

@app.get('/health')
def health_check():
    return {'health': 'ok'}