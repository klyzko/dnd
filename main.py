import os
import sys

# Добавляем корневую директорию проекта в sys.path
# Это нужно для того, чтобы Python мог найти пакет 'app'
# независимо от того, откуда запускается скрипт.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from dnd.model.tasks import Task
from dnd.repositories import user_registration


import uvicorn
#from app.core.config import settings

app = FastAPI(
    title="Smart Todo Planner",
    description="Умный планировщик задач с AI и Telegram",
    version="1.0.0"
)
def start_app():
    uvicorn.run(app='dnd.main:app', host="0.0.0.0", port=8000, reload=True)
# Подключаем эндпоинты
#app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
#app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
#app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
#app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
#app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(user_registration.router, prefix="/api/users", tags=["users"])
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