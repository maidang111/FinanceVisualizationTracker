from fastapi import FastAPI
from db.database import init_db
from routers import agent, tracker

app = FastAPI(title="Finance Visualization Tracker")


@app.on_event("startup")
def startup():
    init_db()


app.include_router(agent.router)
app.include_router(tracker.router)
