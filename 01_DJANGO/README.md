### Python and Django

This repository will contain a lot of python django examples, applications and api's.

<img src="/1.png" width="100%" alt=""/>

### Getting started

Make sure you have python installed in your computer.

### Creating a Django project

When creating a django project first thing we need to do is creating a virtual environment by running the following command:

```shell
virtualenv <name of the virtual environment>

# example
virtualenv venv
```

The second step is to activate the virtual environment by running the following command:

```shell
.\venv\Scripts\activate
```

Next we are going to install `django` by running the following command:

```shell
pip install django
```

After all these we are now ready to run `django-admin` commands for example creating a new django project we run the following command:

```shell
django-admin startproject <project-name>
# Example
django-admin startproject setup_project
```

Next we will navigate to a location where our project is for example:

```shell
cd setup_project
```

### Directory tree structure

By running the command:

```shell
django-admin startproject setup_project
```

django will create a boiler plate files for a new django application with files and folders. The default file and folders represented in a tree structure will be looking as follows:

```shell
📁 00_SETUP
    📁 setup_project
        📁 setup_project
            - __init__.py
            - asgi.py
            - settings.py
            - urls.py
            - wsgi.py
        - manage.py
```

We will get to know each file in depth as we go in different sections of this repository. Next we need to start the django application. To start the django application make sure you navigate to where the file `manage.py` is and run the following command:

```shell
python manage.py runserver
```

The local server will start at a default port of `8000` and to see the website you visit http://localhost:8000 or http://127.0.0.1/8000.

> Note that by default django represent an `admin` interface to us which can be accessed by going to http://localhost:8000/admin or http://127.0.0.1/8000/admin

### Refs.

- [Django Documentation](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
