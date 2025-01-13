
from graphene_django import DjangoObjectType
from api.models import Todo
from graphene import ObjectType, String, Boolean, Field, List, Int

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__' #("id", "completed", "created_at", 'title')
        
        
class ErrorType(ObjectType):
    field = String(required=True)
    message = String(required=True)
    
    
class TodoResponseType(ObjectType):
    error = Field(ErrorType, required=False)
    ok = Boolean(required=True)
    todo = Field(TodoType, required=False)
    
class TodosResponseType(ObjectType):
    error = Field(ErrorType, required=False)
    ok = Boolean(required=True)
    todos = List(TodoType, required=False)
    total = Int(required=True)
    