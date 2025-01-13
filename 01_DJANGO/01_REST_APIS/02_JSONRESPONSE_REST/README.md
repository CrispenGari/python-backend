### Rest API using `JsonResponse`

In this one we are going to create a rest api by persisting the data into the database. We aew going to avoid the make use of the `rest_framework` and use what we call the `JsonResponse` from `django.http`. We are going to do something similar to what we did last time:

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

    def to_json(self):
        return {
            'id': self.id, 'title': self.title,
            'created_at': self.created_at, 'completed': self.completed
        }
```

> Our model will contain a `to_json` method that will convert our model object to `json` serializable dictionary.

Now that we have created our model we need to run migrations so that our database table will be created. But before we do that we need to open the `todorest/settings.py` and add the following in the installed apps array:

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig'
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

```py

import json
from django.http import JsonResponse
from api.models import Todo
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def getTodos(request):
    if request.method == 'GET':
        try:
            todos = list(map(lambda x: x.to_json(), Todo.objects.all()))
            return JsonResponse({
                'code': 200,
                'message': 'Getting all Todos.',
                'timestamp': datetime.datetime.now(),
                'todos': todos,
            }, safe=True)
        except Exception as e:
            return  JsonResponse({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            })
    else:
        return JsonResponse({
            'code': 405,
            'message': 'Only GET method is allowed.',
            'timestamp': datetime.datetime.now(),
        })

def getTodo(request, id):
    if request.method == 'GET':
        try:
            todo = Todo.objects.get(id=id)
            return JsonResponse({
                'code': 200,
                'message': 'Getting all Todos.',
                'timestamp': datetime.datetime.now(),
                'todo': todo.to_json(),
            })
        except Todo.DoesNotExist:
            return  JsonResponse({
                'code': 404,
                'message': f'Todo of id {id} was not found.',
                'timestamp': datetime.datetime.now(),
                'todo': None
            })
        except:
            return  JsonResponse({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            })
    else:
        return JsonResponse({
            'code': 405,
            'message': 'Only GET method is allowed.',
            'timestamp': datetime.datetime.now(),
        })

@csrf_exempt
def deleteTodo(request, id):
    if request.method == 'DELETE':
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()
            return JsonResponse({
                'code': 204,
                'message': 'Deleted todo of id {id}.',
                'timestamp': datetime.datetime.now(),
                'todo': None,
            })
        except Todo.DoesNotExist:
            return  JsonResponse({
                'code': 404,
                'message': f'Todo of id {id} was not found.',
                'timestamp': datetime.datetime.now(),
                'todo': None
            })
        except:
            return  JsonResponse({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            })
    else:
        return JsonResponse({
            'code': 405,
            'message': 'Only DELETE method is allowed.',
            'timestamp': datetime.datetime.now(),
        })

@csrf_exempt
def updateTodo(request, id):
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            todo = Todo.objects.get(id=id)
            data = json.loads(request.body.decode('utf-8'))
            todo.completed = data['completed'] if data['completed'] else todo.completed
            todo.title = data['title'] if data['title'] else todo.title
            todo.save()
            return JsonResponse({
                'code': 200,
                'message': 'Updated Todo of id {id}.',
                'timestamp': datetime.datetime.now(),
                'todo': todo.to_json(),
            })
        except Todo.DoesNotExist:
            return  JsonResponse({
                'code': 404,
                'message': f'Todo of id {id} was not found.',
                'timestamp': datetime.datetime.now(),
                'todo': None
            })
        except:
            return  JsonResponse({
                'code': 500,
                'message': 'Internal Server Error.',
                'timestamp': datetime.datetime.now(),
            })
    else:
        return JsonResponse({
            'code': 405,
            'message': 'Only PUT or PATCH method(s) are allowed.',
            'timestamp': datetime.datetime.now(),
        })

@csrf_exempt
def addTodo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            todo = Todo(title=data['title'], completed=data['completed'])
            todo.save()
            return JsonResponse({
                'code': 201,
                'message': 'Created Todo.',
                'timestamp': datetime.datetime.now(),
                'todo': todo.to_json(),
            })
        except Exception as e:
            print(e)
            return  JsonResponse({
                'code': 500,
                'message': 'Internal Server Error.'
            })
    else:
        return JsonResponse({
            'code': 405,
            'message': 'Only POST method is allowed.'
        })
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

> _Note that using the `djangorestframework` allows us to serializable our models very easily but we can use the `JsonResponse` from pure `django` framework as we did._
