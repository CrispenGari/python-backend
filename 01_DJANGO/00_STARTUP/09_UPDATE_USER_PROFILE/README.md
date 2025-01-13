### UPDATE USER PROFILE

In this section we are going to learn how to implement the user upload profile. We are going to continue from where we left in the previous section and create a user profile form where users will be able to update their profile on their own.

First we are going to open a `users/forms.py` and create a model form of both the profile and the user. So our `users/forms.py` file will have the following code in it.

```py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
```

> It is very inefficient to store the large images in so we can resize all the images that have either width and height that is greater than `300px` to have the width and height of `300px` so to do this we need to overide the `save` method in the profile model as follows:

```py
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
```

This function:

```py
def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
```

Will save all the images that has width or height greater than 300px as small images.

Next we are going to open the `views.py` so that we will display the user_form and profile_form as a single form. We are also going to use of the `instance` keyword arg so that we will populate the model form with some current values. Our views.py file will look as follows:

```py
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            messages.success(request, f'Account created for {username}, Now you can login to the app!')
            return redirect('login')
    return render(request, "users/register.html", context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
```

> Not that the `req.user` will return the authenticated user. In the `ProfileUpdateForm` we also need to pass in the `request.FILES`, so that we will accept files on upload.

### Profile template

We are going to change the profile template, from the previous one just by adding the `form` and on the form we must add `enctype` attribute as `multipart/form-data`. So our `profile.html` will look as follows:

```html
{% extends "blog/base.html" %} {% load crispy_forms_tags %} {% block content %}
<div class="content-section">
  <div class="media">
    <img
      class="rounded-circle account-img"
      src="{{ user.profile.image.url }}"
    />
    <div class="media-body">
      <h2 class="account-heading">{{ user.username }}</h2>
      <p class="text-secondary">{{ user.email }}</p>
    </div>
  </div>
  <form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <fieldset class="form-group">
      <legend class="border-bottom mb-4">Profile Info</legend>
      {{ u_form|crispy }} {{ p_form|crispy }}
    </fieldset>
    <div class="form-group">
      <button class="btn btn-outline-info" type="submit">Update</button>
    </div>
  </form>
</div>
{% endblock content %}
```

> Lastly we are going to display the user avatar on the blog post. So we are going to `blog/templates/blog/home.html` and modify it to look as follows:

```html
{% extends "blog/base.html" %} {% load static %} {% block title %}
<title>{{ title }}</title>
{% endblock title%} {% block content %} {% for post in posts %}
<article class="media content-section">
  <img
    class="rounded-circle article-img"
    src="{{ post.user.profile.image.url }}"
  />
  <div class="media-body">
    <div class="article-metadata">
      <a class="mr-2" href="#">{{ post.user.username }}</a>
      <small class="text-muted">{{ post.created_at|date:"F d, Y" }}</small>
    </div>
    <h5><a class="article-title" href="#">{{ post.title }}</a></h5>
    <p class="article-content">{{ post.content }}</p>
  </div>
</article>
{% endfor %} {% endblock content %}
```

### Next

In the next section we are going to look on how to update, delete, and create posts from the forms.

### Ref

1. [django: signals](https://docs.djangoproject.com/en/4.0/ref/signals/)
