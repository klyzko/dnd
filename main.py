import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from dependency.depend_redis import lifespan
from api.v1.router import users, tasks
from core.logger_config import logg



from fastapi import FastAPI
#from .model.tasks import Task
#from .application import user_registration


import uvicorn
#from app.core.config import settings

app = FastAPI(
    title="Smart Todo Planner",
    description="Умный планировщик задач с AI и Telegram",
    version="1.0.0",
    lifespan=lifespan
)
def start_app():
    logg
    uvicorn.run(app='dnd.main:app', host="127.0.0.1", port=8000, reload=True)
# Подключаем эндпоинты

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.post("/")
async def root():
    return {
        "message": "Welcome to Smart Todo Planner API",
        "docs": "/docs",
        "redoc": "/redoc",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    start_app()