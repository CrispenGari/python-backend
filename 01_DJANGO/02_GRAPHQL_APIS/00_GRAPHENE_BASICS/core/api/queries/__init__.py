
from api.models import Todo
from graphene import ObjectType, String, NonNull, Field, Argument
from api.types.input import GetTodoInputType
from api.types.object import TodoResponseType, TodosResponseType, ErrorType

class Query(ObjectType):
    hello = String(default_value="Hi!")
    todos = Field(NonNull(TodosResponseType))
    todo =Field(TodoResponseType, input=Argument(GetTodoInputType, required=True))
    
    def resolve_todos(root, info):
        res = Todo.objects.all()
        _len = len(res)
        ok = True
        return TodosResponseType(
            ok=ok,
            total=_len,
            error=None,
            todos = res
        )
        
    def resolve_todo(root, info, input):
        res = Todo.objects.get(id=input.get('id'))
        if res:
            ok = True
            return TodoResponseType(
                ok=ok,
                error=None,
                todo = res
            )
        else:
            error = ErrorType(
                message= f"Todo of that id '{input.get('id')}' was not found.",
                field = "id"
            )
            ok = True
            return TodoResponseType(
                ok=ok,
                error=error,
                todo = None
            )
