### User Registration Form

In this section we are going to see how we can implement the user Registration form. We are going to use [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) to design our registration form and intergrade it with bootstrap 4.

### Getting started

First we are going to create a new django app called `users` in by running the following command:

```shell
python manage.py startapp users
```

In this application we are going to handle all the authentication and link it to our blog application. Note that this is the continuation from the previous section where we load bootstrap and show how to load static files in templates.

We will then go and add our `users` app in the `settings.py` under `INSTALLED_APPS` list as follows:

```py
INSTALLED_APPS = [
    ...
    'users.apps.UsersConfig',
    ...
]

```

### Installation of django-crispy-forms

Before we get any deep we need to install `django-crispy-forms` by running the following command:

```shell
pip install django-crispy-forms
```

We will then go and add our `crispy-forms` app in the `settings.py` under `INSTALLED_APPS` list as follows:

```py
INSTALLED_APPS = [
    ...
    'crispy_forms',
    ...
]
```

### Templates

We are going to create templates for our `users` app, so we will create a directory called `templates/users` where all our templates will be.

1. register.html

Note that our `register.html` is extending the `base.html` from the `blog` app because these apps belongs to the same project, and django knows how to handle this.

```html
{% extends "blog/base.html" %} {% load crispy_forms_tags %} {% block content %}
<div class="content-section">
  <form method="POST">
    {% csrf_token %}
    <fieldset class="form-group">
      <legend class="border-bottom mb-4">CREATE ACCOUNT</legend>
      {{ form|crispy }}
    </fieldset>
    <div class="form-group">
      <button class="btn btn-outline-info" type="submit">REGISTER</button>
    </div>
  </form>
  <div class="border-top pt-3">
    <small class="text-muted">
      Already Have An Account? <a class="ml-2" href="#">LOGIN</a>
    </small>
  </div>
</div>
{% endblock content %}
```

We are also loading `crispy_forms_tags` so that our form will be styled nicely.

### Register form

We are going to create the `forms.py` file in the `users` application. In this file we will be able to customize the default django registration (UserCreationForm). So we are going to inherit some of the fields of `UserCreationForm` and add one more field `email` as follows.

```py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

### Register view.

We are then going to open the `users/views.py` and create a `register` view as follows:

```py
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
# Create your views here.

def register(request):
    context = {
        "form": UserRegisterForm()
    }
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            # save to the database
            form.save()
            username = form.cleaned_data.get('username')
            # message flashing
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    return render(request, "users/register.html", context)
```

- We are going to create a `UserRegisterForm()` for any request method that will come
- If the request method is `POST` then we may want to create the user but when we don't have errors.
- If the form is valid we then save the user credentials to the database and flush message telling that their account has been created.
- We don't want to show the user the registration page when they are registered therefore we will redirect them to the `home` page.

Next we are going to open the `urls.py` of the project and register our `register` view as follows:

```py
from django.contrib import admin
from django.urls import path, include
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name="register"),
    path('', include('blog.urls'))
]
```

### Flashing messages to the frontend

We need to go to our `base.html` file and add the following piece of code to where we want our flashed messages to be displayed:

```html
{% if messages %} {% for message in messages %}
<div class="alert alert-{{ message.tags }}">{{ message }}</div>
{% endfor %} {% endif %}
```

We will then go to the `settings.py` and add the following `CRISPY_TEMPLATE_PACK` config at the bottom of the file:

```py
STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

Now the user can register and if you visit the `/admin` route you will be able to see the new created user.

### Next.

In the next section we are going to look at how to do the login and logout functionality. We are going to continue from here.

### Ref

1. [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
