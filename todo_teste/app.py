from fastapi import FastAPI

from todo_teste.routers import users

app = FastAPI()

app.include_router(users.router)
