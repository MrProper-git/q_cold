import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers.leads import leads
from routers.admin import admin
from app.shared.database import setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускается ПЕРЕД тем, как сервер начнет принимать запросы
    await setup_database()
    print("✅ Database tables created")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(leads)
app.include_router(admin)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)