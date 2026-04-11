from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import init_db
from routers import agent, tracker


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Finance Visualization Tracker", lifespan=lifespan)

app.include_router(agent.router)
app.include_router(tracker.router)
