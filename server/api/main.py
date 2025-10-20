from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from core.config import settings
from core.database import engine, Base
from utils.print_logs_console import print_error, print_success, print_info


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")

    # Создаем таблицы
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print_success("Подключение к БД установлено")
    except Exception as e:
        print_error("Ошибка подключения к БД")
        print_error(e)
    finally:
        print_info("Приложение запущено")
        yield

    # Shutdown code
    print("Shutting down...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION_API,
    lifespan=lifespan,
)

@app.get("/")
def read_root():
    return HTMLResponse("MyPBX API is up and running!")



