from fastapi import APIRouter
userRouter = APIRouter(
    prefix="/api/v1/users",

)

people = [
    {'name': "Jonh", "gender": "M", "age": 16, 'id': 1},
    {'name': "Peter", "gender": "M", "age": 16, 'id': 2},
]

@userRouter.get('/')
def users():
    return people