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

