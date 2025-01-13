### ORM Databases and Migrations

In this section we are going to create create our first model using Object Relational Mapping (orms) in django.

We are going to create a simple one to many relationship between the user and the post. The relationship will be defined as the user having many post and a many post which belongs to a single user.

We are going to learn how to use the interactive python shell from django to insert and query data from the database.

We are also going to query the posts with python code and display them on templates.

### Creating a Post model

To create models we will open the `models.py` file and create class `Post` and specify fields and relationships.

```py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
```

- We are creating a model called `Post` using orm approach.
- We are then going to define the fields we want our Post model to have.
- We are relating the `Post` model with the default `User` model from `django` with a `ForeignKey` attribute on user and we are setting `on_delete` to `CASCADE` because we want to delete the post of the user as well as soon as we delete the user.

> Note that whenever you make changes to the `models.py` we need to create and run migrations. So in the command line we are going to run the following commands to create and run migrations respectively

```shell
python manage.py makemigrations

python manage.py migrate
```

### Using the Interactive Shell.

In this subsection of the README we are going to learn how to use the interactive shell to create, delete, update and query data from our database.

Firstly, we need to connect to the `django-python-shell` by running the following command:

```shell
python manage.py shell
```

Next we need to import all the models that we are going to use as follows.

```py
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
```

1. Getting all the posts and users.

To get all the posts in the database we run the following command:

```shell
>>> Post.objects.all()
<QuerySet []>

# Users
>>> User.objects.all()
<QuerySet [<User: root>]>
```

2. Getting the first user in the users list.

```shell
>>> User.objects.first()
<User: root>
```

3. Using the `get` to get the user by id.

```shell
>>> User.objects.get(id=1)
<User: root>
```

4. Using the filter

```shell
>>> User.objects.filter(username="root")
<QuerySet [<User: root>]>
```

> Note that the `filter` method returns a list of result. So to get the first document in the list we use the `.first()` method as follows:

```shell
>>> User.objects.filter(username="root").first()
<User: root>
```

5. Accessing the data of the user object.

To access the data that is stored in the user object for example we can do it as follows:

```shell
>>> user = User.objects.filter(username="root").first()
>>> user.id
1
# Getting the primary key on the user
>>> user.pk
1
>>> user.username
'root'
```

6. Creating a post.

To create a new post we can do it as follows:

```shell
>>> post_1 = Post(title="Post 1", content="Post 1 content", user=user)
>>> post_1.save()
```

Now if we query all the post we should see that we have a new post.

```shell
>>> Post.objects.all()
<QuerySet [<Post: Post 1>]>
```

7. Updating a post

To update a post we are going to do it as follows:

- first we need to find the post that we want to update
- we then set the new values for fields
- finally we will save the post

The following is an example on how we can update a post with id 1.

```shell
>>> post = Post.objects.get(id=1)
>>> post.title = "Post 1 Updated"
>>> post.content = "Content 1 Updated"
>>> post.save()
```

8. Deleting a post

- To delete a post is simple as calling the `delete` method on the current post.

```shell
>>> post = Post.objects.get(id=1)
>>> post.delete()
(1, {'blog.Post': 1})
```

### Passing the data from database to templates.

In this section we are going to show how we can programatically query the data from the database in `views` and pass it down to templates. In the `views.py` we are going to add the following snippet of code:

```py

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
    pass
```

In our `home.html` template we are going to add the following code to it:

```shell
{% extends "blog/base.html" %} {% block title %}
<title>{{ title }}</title>
{% endblock title%} {% block content %}
<h1>Posts</h1>

{% for post in posts %}
<div>
  <h1>{{ post.title }} * {{ post.created_at|date:"M d, Y"}}</h1>
  <p>{{ post.title }}</p>
  <p>by: {{post.user.username}}</p>
</div>
{% endfor %} {% endblock content %}

```

### Admin and Models

By default if we go to `/admin` on our site we won't be able to see the `Post` model, The reason is very simple we have to register all or models in the `admin.py` file as follows

```py
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```

### Next

In the next section we are going to look at how we can load static files in our templates. Example of templates include:

1. css
2. images
3. javascript
4. etc

We are also going to load `bootstrap` cdn's in our templates.

### Refs.

1. [models](https://docs.djangoproject.com/en/4.0/topics/db/models/)
2. [medium.com](https://medium.com/@ksarthak4ever/django-models-and-shell-8c48963d83a3)
