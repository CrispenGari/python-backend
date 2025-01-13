### Templates

In this section we are going to look on how to render templates in our blog application and how to pass data to templates as well as how to do template inheritance.

> This section is just a continuation from the previous section on how to do basic routing and creation of django applications.

The first thing that we need to do is to register our application `blog` for that we are going to go to the `templates/blog/apps` and it looks as follows:

```py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

```

As we can see `BlogConfig` class is inheriting from `AppConfig` so we will copy the class name "BlogConfig" and go to the `/templates/settings.py` under installed application list we are going to add the following in the list:

```py
"blog.apps.BlogConfig"
```

So that the `INSTALLED_APPS` list will look as follows:

```py
...
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
...
```

Our folder structure before creating adding templates looks as follows:

```
📁 02_Templates
    📁 templates
        📁 blog
            📁 __pycache__
            📁 migrations
        📁 templates

```

Inside the `blog` we are going to create a folder called `templates` and inside the `templates` folder we are going to create another folder with the same name as the `application` name in our case it's `blog`. This allow django to pickup all the template that belongs to `blog` application. So our folder structure will look as follows after creation of these folders:

```
📁 02_Templates
    📁 templates
        📁 blog
            📁 __pycache__
            📁 migrations
            📁 templates
                📁 blog
                    ...(html)
        📁 templates
```

We are going to create two templates which are `home.html` and `about.html` and they will have the following code in them:

1. about.html

```html
<!-- about.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>About</title>
  </head>
  <body>
    <h1>About</h1>
  </body>
</html>
```

2. home.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Home</title>
  </head>
  <body>
    <h1>Home Page</h1>
  </body>
</html>
```

Next we are going to go to the `views.py` and modify it to render html pages for the about and home pages respectively.

```py
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html' )
```

### Passing Data to templates

In this subsection we are going to pass data down to templates using and render the data on the web page.

In our `view.py` of the `blog` app we are going to modify it to look as follows:

```py
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
```

Now we will modify our and render the data respectively as follows:

1. about.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>About</h1>
  </body>
</html>
```

2. home.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>Posts</h1>
    {% for post in posts %}
    <div>
      <h1>{{ post.title }} * {{ post.gender }}</h1>
      <p>{{ post.content }}</p>
      {% if post.isAdmin %}
      <p>Admin</p>
      {% else %}
      <p>Not Admin</p>
      {% endif %}
    </div>
    {% endfor %}
  </body>
</html>
```

Without styling the templates, we are able to see that all the content is rendered as expected.

### Template inheritance

If we look at the `about.html` and `home.html` we are able to see that we are repeating our selfs, (dry). So we want to create a `base.html` file which will contain the code that is common in these two templates. The `about.html` and `home.html` will then inherit from `base.html` file. So our base.html will be looking as follows:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% block title %} {% endblock title %}
  </head>
  <body>
    {% block content %} {% endblock content %}
  </body>
</html>
```

Now the `about.html` will be looking as follows:

```html
{% extends "blog/base.html" %} {% block title %}
<title>{{ title }}</title>
{% endblock title%} {% block content %}
<h1>About Page</h1>
{% endblock content %}
```

And the `home.html` will be looking as follows:

```html
{% extends "blog/base.html" %} {% block title %}
<title>{{ title }}</title>
{% endblock title%} {% block content %}
<h1>Posts</h1>
{% for post in posts %}
<div>
  <h1>{{ post.title }} * {{ post.gender }}</h1>
  <p>{{ post.content }}</p>
  {% if post.isAdmin %}
  <p>Admin</p>
  {% else %}
  <p>Not Admin</p>
  {% endif %}
</div>
{% endfor %} {% endblock content %}
```

> With template inheritance we end up writing cleaner templates without repeating ourselves.

### Ref

1. [templates](https://docs.djangoproject.com/en/4.0/topics/templates/)
