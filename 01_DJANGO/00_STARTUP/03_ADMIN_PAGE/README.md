### Admin Page

In this one we are going to have a quick introduction to the admin interface in a django application.

After creating a django project by default we have access to the `/admin` route which represent us with a simple admin login page. But how can we login into the admin site without creating an admin?

If we start the application with the following command:

```shell
python manage.py runserver
```

And go to http://127.0.0.1:8000/admin/ we will be represented with admin login form. Now we need to create admin credentials by running the following command:

```shell
python manage.py createsuperuser
```

> Note that we need to create migrations first before running this command.

```shell
python manage.py makemigrations
```

> To apply migrations we also need to run the following command:

```shell
python manage.py migrate
```

When you run the following command:

```shell
python manage.py createsuperuser
```

You will be represented with some prompt to for username, password and email. Type those credentials in and they will be used to login in the admin site.

If everything went well we will be able to be logged in into the admin site.

### Next

In the next section we are going to start working with database models.
