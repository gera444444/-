from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.models import Base
from app.api import auth, users, items
from app.websocket import chat

# Создаем таблицы в БД (для SQLite)
Base.metadata.create_all(bind=engine)

# Инициализация приложения
app = FastAPI(
    title="PetShop API",
    description="API для интернет-магазина товаров для животных",
    version="1.0.0",
    docs_url="/docs",         
    redoc_url="/redoc",       
    openapi_url="/openapi.json"
)
from fastapi.staticfiles import StaticFiles
import os

# Путь к фронтенду
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Раздача статики
app.mount("/static", StaticFiles(directory=frontend_path), name="static")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Аутентификация"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Пользователи"])
app.include_router(items.router, prefix="/api/v1/items", tags=["Товары"])
app.include_router(chat.router, prefix="/api/v1/ws", tags=["WebSocket"])

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Добро пожаловать в PetShop API",
        "docs": "/api/v1/docs",
        "redoc": "/api/v1/redoc"
    }

@app.get("/api/v1/healthcheck", tags=["Система"])
async def healthcheck():
    return {"status": "OK"}