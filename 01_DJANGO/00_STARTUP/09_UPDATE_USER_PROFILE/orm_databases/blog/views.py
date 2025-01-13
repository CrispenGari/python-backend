
from django.shortcuts import render
from .models import Post
# Create your views here.

def home(req):
    context ={
        "title": "Home - Posts",
        "posts": Post.objects.all()
    }
    return render(req, 'blog/home.html', context)

def about(req):
    context ={
        'title': 'About'
    }
    return render(req, 'blog/about.html',context)