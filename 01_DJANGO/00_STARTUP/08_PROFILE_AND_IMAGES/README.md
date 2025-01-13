### PROFILE AND IMAGES

In this section we are going to create learn how to work with images in django for our profile update. We are going to continue from the previous section and modify it so that we come up with what we need.

### Profile model

We are going to create a `Profile` model in the `user` application in the file called `models.py` we are then going to create it so that it will have a relationship with the `user` model. The `models.py` will look as follows:

```py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
```

We are setting the `on_delete` to `Cascade` so that when we delete the user, we are also going to delete all the child relationships that it has.

We are then going to create migration migrations by running the following command:

```shell
python manage.py makemigrations
```

Because we are using the `ImageField` we need to install pillow first before running making migrations:

```shell
python -m pip install Pillow
```

To run the migrations we will run the command:

```shell
python manage.py migrate
```

We are then going to open the `settings.py` of the `orm_databases` and add the `MEDIA_ROOT` and `MEDIA_URL` config to the setting.py file as follows:

```py
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

After specifying the `MEDIA_ROOT` and `MEDIA_URL` we are then going to open the `settings.py` and add the following settings.

```py
...
from django.conf import settings
from django.conf.urls.static import static
...
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

Next we are going to register our `Profile` model to the admin interface by opening the `admin.py` in the user app and add the following code:

```py
from django.contrib import admin

from .models import Profile
admin.site.register(Profile)

```

### Profile template

In the `user/templates/user/profile.html` we are going to add the following code as the representation of the profile template.

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
  <!-- FORM HERE -->
</div>
{% endblock content %}
```

### Sending signals

We are going to create a file called `signals.py` in the `user` application an add the following code to it:

```py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

After creating these signals we are going to open the `apps.py` file and add modify it so that it looks as follows:

```py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
```

Now we can now be able to create accounts with default profile pictures and be able to set profile for available users using the admin page.

### Next

In the next section we are going to allow users to update their profile pictures using a form.

### Ref

1. [django: signals](https://docs.djangoproject.com/en/4.0/ref/signals/)
2. [CoreyMSchafer - Github](https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/07-Login-Logout-Authentication/)
