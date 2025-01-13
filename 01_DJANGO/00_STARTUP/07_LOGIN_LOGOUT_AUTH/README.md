### LOGIN LOGOUT AUTHENTICATION

Now that in the previous section we managed to create users, now we want to handle the login and logout functionality. We are going to use the code from the previous section as the base code in this section.

First we are going to create the `login.html` template in the users app as follows:

```html
{% extends "blog/base.html" %} {% load crispy_forms_tags %} {% block content %}
<div class="content-section">
  <form method="POST">
    {% csrf_token %}
    <fieldset class="form-group">
      <legend class="border-bottom mb-4">Login</legend>
      {{ form|crispy }}
    </fieldset>
    <div class="form-group">
      <button class="btn btn-outline-info" type="submit">Login</button>
    </div>
  </form>
  <div class="border-top pt-3">
    <small class="text-muted">
      Want A New Account?
      <a class="ml-2" href="{% url 'register' %}">Register</a>
    </small>
  </div>
</div>
{% endblock content %}
```

We are the going to create the `logout.html` template which will look as follows:

```html
{% extends "blog/base.html" %} {% block content %}
<h5>You are logged out</h2>
<div class="border-top pt-3">
  <small class="text-muted">
    <a href="{% url 'login' %}">Log In Again</a>
  </small>
</div>
{% endblock content %}
```

Lastly we are going to create the `profile.html` template which looks as follows:

```html
{% extends "blog/base.html" %} {% load crispy_forms_tags %} {% block content %}
<div class="content-section">
  <div class="media">
    <div class="media-body">
      <h2 class="account-heading">{{ user.username }}</h2>
      <p class="text-secondary">{{ user.email }}</p>
    </div>
  </div>
</div>
{% endblock content %}
```

We are then going to go to the `urls.py` of our project and register routes for

1. login
2. logout
3. profile

as follows:

```py
from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name="register"),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('blog.urls'))
]

```

### profile view

We are going to create the `profile` view in our users app (views.py) as follows:

```py
...
from django.contrib.auth.decorators import login_required
...
@login_required
def profile(request):
    return render(request, 'users/profile.html')
```

- `@login_required` is the annotation or decorator that protect users from accessing the profile template without being authenticated.

Next we are going to the `settings.py` and add the `LOGIN_REDIRECT_URL` and `LOGIN_URL` as follows:

```py
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'
```

- `LOGIN_REDIRECT_URL` - just tells django that the name of the route that we are going to redirect to when we are logged in. Every time the login form submit with valid credentials it will redirect to the specified route name.

- `LOGIN_URL` - tells django the name of the `login` route.

### Next

Next we are going to look on how to set up profile images to the user profile.

### Ref

1. [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
2. [CoreyMSchafer - Github](https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/07-Login-Logout-Authentication/)
