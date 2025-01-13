### Todo Rest API

In this one we are going to create a rest api by persisting the data into the database. After installing required packages we are going to create a new django project by running the following command:

```shell
django-admin startproject todorest
```

So we are going to create an app called `api` by running the following commands:

```shell
cd todorest
# then

python manage.py startapp api
```

Now if we open our `api/models.py` we can create a new `Todo` model as follows:

```py
from django.db import models
from django.utils import timezone
# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.title
```

Now that we have created our model we need to run migrations so that our database table will be created. But before we do that we need to open the `todorest/settings.py` and add the following in the installed apps array:

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework'
]
```

Then run:

```shell
python manage.py makemigrations
# then
python manage.py migrate

```

### Urls

After making migrations, we need to go to the `todorest/urls.py` and add the following in that file:

```py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1', include('api.urls'))
]
```

Because we are including the `urls` file from the `api` we need to create a `api/urls.py` file.

```py
from django.urls import path
from .views import *

urlpatterns = [
    path('todos/all', getTodos),
    path('todo/one/<int:id>', getTodo),
    path('todo/update/<int:id>', updateTodo),
    path('todo/delete/<int:id>', deleteTodo),
    path('todo/add', addTodo),
]
```

After we have created the `urlpatterns` we need to create the following `views`.

1. getTodo
2. getTodos
3. deleteTodo
4. updateTodo
5. addTodo

Before that we need to create a `serializer` of our Todo Model. For that we are going to create a file called `serializers.py` in the `api` folder and add the following code in it.

```py

from rest_framework import serializers
from api.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__' # fields = ['id', 'title', 'created_at', 'completed']
```

Now that we have a `TodoSerializer` we can now go and create our `views` to do the `CRUD` operations on the `Todo` model. Our `views.py` will look as follows:

```py
from django.shortcuts import render
from rest_framework.status import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Todo
from api.serializers import TodoSerializer
import datetime
# Create your views here.

@api_view(['GET'])
def getTodos(request):
    if request.method == 'GET':
        try:
            todos = Todo.objects.all()
            serializer = TodoSerializer(todos, many=True)
            return Response({
                'code': 200,
                'message': 'Getting all Todos.',
                'timestamp': datetime.datetime.now(),
                'todos': serializer.data,
            }, HTTP_200_OK)
        except:
            return  Response({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            }, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'code': 405,
            'message': 'Only GET method is allowed.',
            'timestamp': datetime.datetime.now(),
        }, HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET"])
def getTodo(request, id):
    if request.method == 'GET':
        try:
            todo = Todo.objects.get(id=id)
            serializer = TodoSerializer(todo)
            return Response({
                'code': 200,
                'message': 'Getting all Todos.',
                'timestamp': datetime.datetime.now(),
                'todo': serializer.data,
            }, HTTP_200_OK)
        except Todo.DoesNotExist:
            return  Response({
                'code': 404,
                'message': f'Todo of id {id} was not found.',
                'timestamp': datetime.datetime.now(),
                'todo': None
            }, HTTP_404_NOT_FOUND)
        except:
            return  Response({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            }, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'code': 405,
            'message': 'Only GET method is allowed.',
            'timestamp': datetime.datetime.now(),
        }, HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def deleteTodo(request, id):
    if request.method == 'DELETE':
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()
            return Response({
                'code': 204,
                'message': 'Deleted todo of id {id}.',
                'timestamp': datetime.datetime.now(),
                'todo': None,
            }, HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return  Response({
                'code': 404,
                'message': f'Todo of id {id} was not found.',
                'timestamp': datetime.datetime.now(),
                'todo': None
            }, HTTP_404_NOT_FOUND)
        except:
            return  Response({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            }, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'code': 405,
            'message': 'Only DELETE method is allowed.',
            'timestamp': datetime.datetime.now(),
        }, HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT', 'PATCH'])
def updateTodo(request, id):
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            todo = Todo.objects.get(id=id)
            serializer = TodoSerializer(todo, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': 'Updated Todo of id {id}.',
                    'timestamp': datetime.datetime.now(),
                    'todo': serializer.data,
                }, HTTP_200_OK)
            else:
                 return Response({
                    'code': 500,
                    'message': 'Invalid data.',
                    'timestamp': datetime.datetime.now(),
                    'todo': None,
                }, HTTP_500_INTERNAL_SERVER_ERROR)
        except Todo.DoesNotExist:
            return  Response({
                'code': 404,
                'message': f'Todo of id {id} was not found.',
                'timestamp': datetime.datetime.now(),
                'todo': None
            }, HTTP_404_NOT_FOUND)
        except:
            return  Response({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            }, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'code': 405,
            'message': 'Only PUT or PATCH method(s) are allowed.',
            'timestamp': datetime.datetime.now(),
        }, HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["POST"])
def addTodo(request):
    if request.method == 'POST':
        try:
            serializer = TodoSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 201,
                    'message': 'Created Todo.',
                    'timestamp': datetime.datetime.now(),
                    'todo': serializer.data,
                }, HTTP_201_CREATED)
            else:
                 return Response({
                    'code': 500,
                    'message': 'Invalid data.',
                    'timestamp': datetime.datetime.now(),
                    'todo': None,
                }, HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return  Response({
                'code': 500,
                'message': 'Internal Server Error.'
            }, HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'code': 405,
            'message': 'Only POST method is allowed.'
        }, HTTP_405_METHOD_NOT_ALLOWED)
```

Now with this we will be able to perform `CRUD` operations and persisting data to the database. The available request url's are:

```shell
GET http://127.0.0.1:8000/api/v1/todo/one/2
GET http://127.0.0.1:8000/api/v1/todo/all
POST http://127.0.0.1:8000/api/v1/todo/add
DELETE http://127.0.0.1:8000/api/v1/todo/delete/2
PATCH http://127.0.0.1:8000/api/v1/todo/update/2
# where 2 is the id of the todo in the database.
```

### Changing the default port of the server.

During starting the server you can specify the port number as follows

```shell
python manage.py runserver 3001
```
