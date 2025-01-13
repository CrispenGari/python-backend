### Simple Rest

In this repository we are going to create a simple rest API in Django using the [django-rest-framework](https://www.django-rest-framework.org/tutorial/quickstart/#serializers).

### Creating a virtual environment

```shell
virtualenv venv
```

### Activating a virtual environment

```shell
.\venv\Scripts\activate
```

### Installing packages

We are going to install two packages which are:

1. `django`
2. `djangorestframework`

```shell
pip install django djangorestframework
```

### Creating a Django Project

Now that we have installed django we can now create a new django project by running the following command:

```shell
django-admin startproject simplerest
```

### Creating an API

First we need to go to the `settings.py` file in the `simplerest` and add `rest_framework` under installed app array as follows:

```py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
]
...
```

Next we are going to create a new folder called `api`. We are going to make this folder a package by creating a `__init__.py` file. Inside that folder we are going to create a file called `urls.py` and another one called `views.py`

### urls.py

```py
from django.urls import path
from .views import *

urlpatterns = [
    path('todos/all', getTodos),
    path('todo/<int:id>', getTodo),
    path('todo/<int:id>', updateTodo),
    path('todo/add', addTodo),
]
```

### views.py

Our views will be functional views and they look as follows

```py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

todos =[{'title': 'cooking', 'completed': False, 'id': 0}, {'title': 'coding', 'completed': False, 'id': 1}]

@api_view(["GET"])
def getTodos(request):
    return Response(todos, status=status.HTTP_200_OK)

@api_view(["GET"])
def getTodo(request, id):
    try:
        todo = list(filter(lambda x: x['id']==id, todos))[0]
        return Response(todo, status=status.HTTP_200_OK)
    except IndexError:
        return Response({'status': 404,
                         "message": f"Todo with the id '{id}' not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def updateTodo(request, id):
    if request.method == "PUT":
        try:

            todo = list(filter(lambda x: x['id']==id, todos))[0]
            todo['completed'] = request.data['completed']
            todo['title'] = request.data['title']
            todos[id] = todo
            return Response(todo, status=status.HTTP_200_OK)
        except IndexError:
            return Response({'status': 404,
                            "message": f"Todo with the id '{id}' not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
       return Response({'status': 400,
                            "message": f"Only Put Method is allowed."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addTodo(request):
    if request.method == "POST":
        try:

            todo = request.data
            todo['id'] = len(todo)
            todos.append(todo)
            return Response(todo, status=status.HTTP_201_CREATED)
        except IndexError:
            return Response({'status': 500,
                            "message": f"Internal Sever Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
       return Response({'status': 400,
                            "message": f"Only Put Method is allowed."}, status=status.HTTP_400_BAD_REQUEST)

```

### simplerest/url.py

In our simplerest/url.py file we are going to include the url of the `api`

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls'))
]

```

Now if we start the server by running the following command:

```shell
python manage.py runserver
```

We will be able to send request to the server at `http://127.0.0.1:8000/`

> Next we are going to create a Todo API that will be connected to a database.

### Refs

1. [django-rest-framework](https://www.django-rest-framework.org/tutorial/quickstart/#serializers).
