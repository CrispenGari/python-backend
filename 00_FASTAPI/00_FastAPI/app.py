from fastapi import FastAPI, Path
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My API",
    description="This is a simple api",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def hi():
    return {'message': 'hi'}


@app.get('/bye')
def bye():
    return {'message': 'bye'}

@app.get('/hello/{name}')
def hello(
    name: Annotated[str, Path()] | None = None
):
    if name is None:
        return {"message": "Hello World"}
    return {'message': f'Hello {name}.'}