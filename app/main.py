from fastapi import FastAPI
from app.api.v1.endpoints import bandit
from app.core import storage
from app.dependencies import bandit_db

app = FastAPI()


@app.on_event("startup")
def load_bandits():
    bandit_db.clear()
    bandit_db.update(storage.load_all_bandits())


app.include_router(bandit.router, prefix="/api/v1/bandit")
