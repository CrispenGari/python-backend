from graphene import ObjectType, Schema

from api.mutations import CreateTodo, UpdateTodo, DeleteTodo
from api.queries import Query

class Mutation(ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

schema = Schema(query=Query, mutation=Mutation)