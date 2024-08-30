from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import config
from database import init_db, teardown
from routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO Add loguru
    print("start app")
    await init_db()
    yield
    await teardown()
    print("stop app")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


for route in routers:
    app.include_router(route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("app:app", host=config.api.host, port=config.api.port, reload=True)
