
from django.shortcuts import render

posts = [
    {
        "username": "username1",
        "isAdmin": True,
        "content": "first post.",
        "gender": "male"
    },
    
    {
        "username": "username2",
        "isAdmin": False,
        "content": "second post.",
        "gender": "female"
    },
    
]
# Create your views here.

def home(request):
    context ={
        "posts": posts,
        "title": "Home Page - Post"
    }
    return render(request, 'blog/home.html', context)

def about(request):
    context ={
        "title": "About Page"
    }
    return render(request, 'blog/about.html', context )