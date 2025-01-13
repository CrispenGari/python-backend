### GraphQL and Django

In this practical example we are going to learn how we can create a graphql api using `Graphene` and `Django`.

### Installation of packages

The following packages are going to be installed in order for us to create our `graphql api` in django:

```shell
pip install graphene-django django
```

### Creating a new Django projects

After we have installed our packages we want to create a new django project by running the following command:

```shell
django-admin startproject core
# then
cd core
```

Then we need to create a new django app called `api` which is our graphql api.

```shell
python manage.py startapp api
```

Now we will need to open the `core/core/settings.py` file and add the following under the installed apps list:

```py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'graphene_django'
]
...
```

Then after that we will need to define the `url` pattens in our `core/core/urls.py` as follows:

```py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', include('api.urls'))
]
```

In our `api/urls.py` file we are going to have the following code in it:

```py
from django.urls import path
from graphene_django.views import GraphQLView
from api.schema import schema

urlpatterns = [
    path("", GraphQLView.as_view(graphiql=True, schema=schema)),
]
```

We are making the `GraphQLView` to be a view. We are setting the `graphiql` to true because we want the graphql playground that allows us to interact with our `api`. And we are also pointing the `schema` to where we are creating our `schema` which is in the file `api/schema.py` which looks as follows:

```py
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")

    def resolve_hello(root, info):
        return "Hello There"

schema = graphene.Schema(query=Query)
```

Alternatively you can open the `core/core/settings.py` and define the schema location as follows

```py
GRAPHENE = {
    "SCHEMA": "api.schema.schema"
}
```

Now if we start the server by running the following command:

```shell
python manage.py runserver 3001
```

If you are getting an error saying:

```shell
ImportError: cannot import name 'force_text' from 'django.utils.encoding'
```

This is an error from `Django` all you have to do is to open your `venv>Lib>site-packages` and locate `graphene_django` and under the `utils/utils.py` change the import from:

```py
from django.utils.encoding import force_text
```

to:

```py
from django.utils.encoding import force_str as force_text
```

And `Save!!`

We can go to `http://localhost:3001/graphql` and get a graphiql interface to start making graphql queries and mutations.

Hello World Query:

```
{
  hello
}
```

Output

```json
{
  "data": {
    "hello": "Hi!"
  }
}
```

### CRUD operations on Todo

Now that we have a graphql endpoint working. Now it's time for us to do `CRUD` operations on todos. We are going to create a `Todo` model in the `api/models.py` as follows:

```py
from django.db import models
from django.utils import timezone
class Todo(models.Model):
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.title

    def to_json(self):
        return {
            'id': self.id, 'title': self.title,
            'created_at': self.created_at, 'completed': self.completed
        }
```

After creating our model we need to run migrations by running the following commands:

```shell
python manage.py makemigrations

python manage.py migrate
```

In our `schema` we are going to have graphql `input` and object `types`. I'm going to create a new package called `types`. In that package we are going to have `input` and `object` sub-packages. Our input types will be in the `input` package and object types will be in our `object` package.

### ObjectTypes

Our Object types looks as follows in the `api/types/object/__init__.py` file

```py

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

```

### InputTypes

Out Input types looks as follows in the `api/types/input/__init__.py` file

```py

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


```

### `schema.py`

Our schema for making CRUD operations on todos looks as follows:

```py
from graphene import ObjectType, String, Schema, Field, NonNull
import graphene

from api.types.input import *
from api.types.object import *
from api.models import Todo

class Query(ObjectType):
    hello = String(default_value="Hi!")
    todos = Field(NonNull(TodosResponseType))
    todo =Field(TodoResponseType, input=graphene.Argument(GetTodoInputType, required=True))

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


class CreateTodo(graphene.Mutation):
    class Arguments:
        input = AddTodoInputType(required=True)

    todo = graphene.Field(NonNull(lambda: TodoResponseType))
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


class UpdateTodo(graphene.Mutation):
    class Arguments:
        input = UpdateTodoInputType(required=True)

    todo = graphene.Field(NonNull(lambda: TodoResponseType))
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


class DeleteTodo(graphene.Mutation):
    class Arguments:
        input = DeleteTodoInputType(required=True)

    todo = graphene.Field(NonNull(lambda: TodoResponseType))
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


class Mutation(ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

schema = Schema(query=Query, mutation=Mutation)
```

### Making GraphQL API Calls

First of all we are going to define the graphql fragments based on our graphql types. Our graphql fragments will look as follows:

```
fragment TodoFragment on TodoType {
  id
  title
  createdAt
  completed
}

fragment ErrorFragment on ErrorType {
  field
  message
}

fragment TodosResponseFragment on TodosResponseType {
  todos {
    ...TodoFragment

  }
  total
  ok
  error {
    ...ErrorFragment
  }
}

fragment TodoResponseFragment on TodoResponseType {
  todo {
    ...TodoFragment
  }
  ok
  error {
    ...ErrorFragment
  }
}

```

> _Note that creating graphql fragments is optional you can query the fields directly._

1. Getting all todos

```
query GetTodos{
  todos{
    ...TodosResponseFragment
  }
}
```

Output:

```json
{
  "data": {
    "todos": {
      "todos": [
        {
          "id": "1",
          "title": "cooking",
          "createdAt": "2022-08-15T11:17:46.257574+00:00",
          "completed": false
        },
        {
          "id": "2",
          "title": "coding",
          "createdAt": "2022-08-15T11:18:55.381373+00:00",
          "completed": false
        },
        {
          "id": "3",
          "title": "running",
          "createdAt": "2022-08-15T11:19:02.424438+00:00",
          "completed": false
        }
      ],
      "total": 3,
      "ok": true,
      "error": null
    }
  }
}
```

2. Getting a single todo.

```

```

Query Variables:

```json

```

Output:

```json

```

3. Creating a single todo

```py
mutation CreateTodo($input: AddTodoInputType!) {
  createTodo(input: $input) {
    todo {
     ...TodoResponseFragment
    }
  }
}

```

Query Variables

```json
{
  "input": {
    "title": "cooking"
  }
}
```

Output

```json
{
  "data": {
    "createTodo": {
      "todo": {
        "todo": {
          "id": "1",
          "title": "cooking",
          "createdAt": "2022-08-15T11:17:46.257574+00:00",
          "completed": false
        },
        "ok": true,
        "error": null
      }
    }
  }
}
```

3. Creating a single todo

```
query GetTodo($input: GetTodoInputType!) {
  todo(input: $input){
    ...TodoResponseFragment
  }
}

```

Query Variables

```json
{
  "input": {
    "id": 2
  }
}
```

Output

```json
{
  "data": {
    "todo": {
      "todo": {
        "id": "2",
        "title": "coding",
        "createdAt": "2022-08-15T11:18:55.381373+00:00",
        "completed": false
      },
      "ok": true,
      "error": null
    }
  }
}
```

4. Updating todo

```
mutation UpdateTodo($input: UpdateTodoInputType!) {
  updateTodo(input: $input){
    todo{
      ...TodoResponseFragment
    }
  }
}
```

Query Variables

```json
{
  "input": {
    "id": 2,
    "title": "coding javascript",
    "completed": true
  }
}
```

Output

```json
{
  "data": {
    "updateTodo": {
      "todo": {
        "todo": {
          "id": "2",
          "title": "coding javascript",
          "createdAt": "2022-08-15T11:18:55.381373+00:00",
          "completed": true
        },
        "ok": true,
        "error": null
      }
    }
  }
}
```

5. Deleting Todo

```
mutation DeleteTodo($input: DeleteTodoInputType!) {
  deleteTodo(input: $input){
    todo{
      ...TodoResponseFragment
    }
  }
}
```

Query Variables

```json
{
  "input": {
    "id": 2
  }
}
```

Output

```json
{
  "data": {
    "deleteTodo": {
      "todo": {
        "todo": null,
        "ok": true,
        "error": null
      }
    }
  }
}
```

### Refactoring the schema.

Our schema.py file is becoming so big. We want to refactor the code by creating two more packages which are:

1. mutations - this package will contain all the mutations that we are going to have in this api.
2. queries- this package will contain all the queries that we are going to have in this api.

Now our `schema.py` file will look as follows:

```py
from graphene import ObjectType, Schema

from api.mutations import CreateTodo, UpdateTodo, DeleteTodo
from api.queries import Query

class Mutation(ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

schema = Schema(query=Query, mutation=Mutation)
```

Then our `mutations/__init__.py` will have the following code in it.

```py

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

```

Then our `queries/__init__.py` will have the following code in it.

```py

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

```

### Refs

1. [graphene-python.org](https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/)
