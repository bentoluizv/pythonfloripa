from fastapi import FastAPI

from src.resources.events.router import router as events_router
from src.resources.users.router import router as users_router

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(users_router)
app.include_router(events_router)
