import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import config
from routers import routers

app = FastAPI()
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
    print(config.api.origins)
    uvicorn.run("app:app", host=config.api.host, port=config.api.port, reload=True)
