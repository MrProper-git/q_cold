import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.leads import leads
from app.api.routers.admin import admin
from app.shared.database import setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):

    await setup_database()
    print("✅ Database tables created")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(leads)
app.include_router(admin)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # пока для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)