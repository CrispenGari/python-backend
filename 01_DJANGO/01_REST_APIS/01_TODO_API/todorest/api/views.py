from django.shortcuts import render
from django.http import JsonResponse
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