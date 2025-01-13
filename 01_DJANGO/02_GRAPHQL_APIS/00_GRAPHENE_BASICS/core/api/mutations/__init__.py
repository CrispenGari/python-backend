
from graphene import Mutation, Field, NonNull
from api.types.input import *
from api.types.object import *

class CreateTodo(Mutation):
    class Arguments:
        input = AddTodoInputType(required=True)

    todo = Field(NonNull(lambda: TodoResponseType))
    def mutate(self, info, input):
        try:
            _todo = Todo(title= input['title'])
            _todo.save()
            todo = TodoResponseType(
                ok =True,
                error= None,
                todo = _todo
            )
            return CreateTodo(todo)
        except Exception as e:
            error = ErrorType(
                message= e,
                field = "todo"
            )
            todo = TodoResponseType(
                ok =False,
                error= error,
                todo = None
            )
            return CreateTodo(todo)


class UpdateTodo(Mutation):
    class Arguments:
        input = UpdateTodoInputType(required=True)

    todo = Field(NonNull(lambda: TodoResponseType))
    def mutate(self, info, input):
        try:
            _todo = Todo.objects.get(id=input.get('id'))
            if _todo:
                _todo.completed = input['completed'] if input['completed'] else _todo.completed
                _todo.title = input['title'] if input['title'] else _todo.title
                _todo.save()
                todo = TodoResponseType(
                    ok= True,
                    error= None,
                    todo = _todo
                )
                return UpdateTodo(todo)
            else:
                error = ErrorType(
                    message= f"Todo of that id '{input.get('id')}' was not found.",
                    field = "id"
                )
                todo = TodoResponseType(
                    ok =False,
                    error= error,
                    todo = None
                )
            return UpdateTodo(todo)
        except Exception as e:
            error = ErrorType(
                message= e,
                field = "todo"
            )
            todo = TodoResponseType(
                ok =False,
                error= error,
                todo = None
            )
            return UpdateTodo(todo)


class DeleteTodo(Mutation):
    class Arguments:
        input = DeleteTodoInputType(required=True)

    todo = Field(NonNull(lambda: TodoResponseType))
    def mutate(self, info, input):
        try:
            _todo = Todo.objects.get(id=input.get('id'))
            if _todo:
                todo = TodoResponseType(
                    ok= True,
                    error= None,
                    todo = None
                )
                _todo.delete()
                return DeleteTodo(todo)
            else:
                error = ErrorType(
                    message= f"Todo of that id '{input.get('id')}' was not found.",
                    field = "id"
                )
                todo = TodoResponseType(
                    ok =False,
                    error= error,
                    todo = None
                )
            return DeleteTodo(todo)
        except Exception as e:
            error = ErrorType(
                message= e,
                field = "todo"
            )
            todo = TodoResponseType(
                ok =False,
                error= error,
                todo = None
            )
            return DeleteTodo(todo)
