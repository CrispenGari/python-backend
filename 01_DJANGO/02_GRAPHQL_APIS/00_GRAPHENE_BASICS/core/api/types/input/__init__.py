
from graphene import String, InputObjectType, Boolean, Int

class AddTodoInputType(InputObjectType):
    title = String(required=True)

class UpdateTodoInputType(InputObjectType):
    title = String(required=False)
    completed = Boolean(required=False)
    id = Int(required=True)
    
class GetTodoInputType(InputObjectType):
    id = Int(required=True)
    
class DeleteTodoInputType(GetTodoInputType):pass
    
