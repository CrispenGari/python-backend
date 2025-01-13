### Applications And Routes

In this section we are going to learn how to work with applications in a django project. We are also going to look at how we can create different routes for those applications later on in this section.

In the previous section we looked on how we can setup the virtual environment and creation of a new django project. A django project can have multiple applications. In this one we are going to take it from where we left from the previous section and show how we can create a django application in our django project.

After activating the virtual environment and installing `django` we are then going to run the following command to create a new django project.

```shell
django-admin startproject application_routes
# change directory to application_routes
cd application_routes
```

### Creating a new django application

To create a new django application we have to navigate to the directory where the file `manage.py` is located and run the following command:

```shell
python manage.py startapp <app_name>
# example
python manage.py startapp blog
```

> In Django project we can have different application. Consider a good example of Facebook. Facebook is a huge web project consist of different applications. We can take feed, market, reels as examples of facebook applications in a facebook project.

After running the above command our directory structure will look as follows:

```
📁 01_APPLICATIONS_AND_ROUTES
    📁 application_routes
        📁 application_routes
            - __init__.py
            ...
        📁 blog
           📁  migrations
           - __init__.py
            ...
        -   manage.py
```

Now you can start the server by running the following command:

```shell
python manage.py runserver
```

### Views

In the `views.py` we will create functions/views that will be able to display html content to the browser based on the specified logic routing. We are going to go to the `views.py` and add the following code to it:

```py
from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("<h1>Home Page</h1>")

def about(request):
    return HttpResponse("<h1>About Page</h1>")
```

### Routing

Our views need to be displayed in the browser somewhere somehow, so we need to handle the routes logic of our application. We will create a file called `urls.py` in the `blog` application and add the following code to it:

```py
from django.urls import path
from .views import home, about

urlpatterns = [
    path('', home, name='blog-home'),
    path('about/', about, name='blog-about')
]
```

Now we have to go to the `application_routes/urls.py` file and include our url patterns for the `blog` application as follows:

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls'))
]
```

Now we will be able to navigate to the following routes and get content in the browser:

1. http://localhost:8000/blog/
2. http://localhost:8000/blog/about/

### Next

In the next section we are going to look on how to render templates in our blog application and how to pass data to templates as well as how to do template inheritence.
