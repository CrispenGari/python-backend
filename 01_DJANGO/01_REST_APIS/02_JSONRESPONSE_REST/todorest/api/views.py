
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