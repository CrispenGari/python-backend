
from django.urls import path
from .views import *

urlpatterns = [
    path('todos/all', getTodos),
    path('todo/<int:id>', getTodo),
    path('todo/<int:id>', updateTodo),
    path('todo/add', addTodo),

]