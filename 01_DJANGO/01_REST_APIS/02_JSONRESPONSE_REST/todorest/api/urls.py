
from django.urls import path
from .views import *

urlpatterns = [
    path('todos/all', getTodos),
    path('todo/one/<int:id>', getTodo),
    path('todo/update/<int:id>', updateTodo),
    path('todo/delete/<int:id>', deleteTodo),
    path('todo/add', addTodo),
]