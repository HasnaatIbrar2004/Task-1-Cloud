from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import models  # noqa: F401  (registers tables)
from database import Base, engine
from v1.admins.router import router as admins_router
from v1.users.router import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Voting System - Auth API", version="1.0.0", lifespan=lifespan)
app.include_router(users_router)
app.include_router(admins_router)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
