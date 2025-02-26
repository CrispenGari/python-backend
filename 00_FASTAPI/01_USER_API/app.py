from fastapi import status
from routers.authRouter import authRouter
from fastapi.responses import JSONResponse
from routers.user import userRouter
from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/storage", StaticFiles(directory="storage"), name="storage")
app.include_router(authRouter)
app.include_router(userRouter)


@app.get("/")
def default():
    return JSONResponse(
        {"message": "This is a users API", "totalUsers": 0},
        status_code=status.HTTP_200_OK,
    )
