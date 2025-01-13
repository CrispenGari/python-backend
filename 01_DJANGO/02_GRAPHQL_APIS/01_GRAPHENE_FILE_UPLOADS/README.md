### GraphQL File Uploads

In this repository we are going to show how we can do file uploads using graphene and django. We will be using [this repository's README](https://github.com/CrispenGari/python-and-django/tree/main/02_GRAPHQL_APIS/00_GRAPHENE_BASICS) as instructions on how to set graphene and django.

### Installation

First we need to install the required packages by running the following command:

```shell
pip install graphene-django django graphene-file-upload pillow
```

Then next we are going to create a `django` project by running the following command:

```shell
django-admin startproject file_uploads
# changing directory to file_uploads

cd  file_uploads
```

Next we are going to create a `django-app` by running the following command

```shell
python manage.py startapp api
```

Next we are going to open our `file_uploads/file_uploads/settings.py` and add the following:

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'graphene_django'
]
```

Next we are going to open our `file_uploads/file_uploads/urls.py` and add the following:

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', include('api.urls'))
]
```

Now in our `api/urls.py` file we are going to create `urlpatterns` as follows for our `graphql` endpoint.

```py
from graphene_file_upload.django import FileUploadGraphQLView

from django.urls import path
from api.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),
]
```

> Note that we are using `csrf_exempt` decorator to avoid the error `Forbidden (CSRF cookie not set.): /graphql/` when uploading files.

Next we will then open the `file_uploads/settings.py` and add the `graphene_django` under installed apps `list` as follows

```py

...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'api.apps.ApiConfig',
]
...
```

If you are getting an error while trying to upload a file you might want to set `APPEND_SLASH` setting to `False` in your `settings.py` before `MIDDLEWARE` as follows:

```py

....

APPEND_SLASH = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'graphene_file_upload',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Upload Mutation

Next we are going to open our `schema.py` file and create an `UploadFileMutation` that allows us to upload a file using graphql.

```py


import graphene
from graphene_file_upload.scalars import Upload
from PIL import Image
import os

class UploadFileMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        file_name = file.name
        image = Image.open(file.file)
        save_path = os.path.join(os.getcwd(), 'images', file_name)
        image.save(save_path)
        return UploadFileMutation(success=True)

class Mutation(graphene.ObjectType):
    uploadFile = UploadFileMutation.Field()

class Query(graphene.ObjectType):
    hello = graphene.String()
    def resolve_hello(root, info):
        return "hello world"

schema = graphene.Schema(query=Query, mutation=Mutation)
```

1. So we are getting the file from the client via graphql
2. We are saving the file in the folder called `images` with it's original name.

After this we can start the server by running the following command:

```shell
python manage.py runserver 3001
```

The server will start at a port of `3001` and we can be able to access the `graphql` server at `http://127.0.0.1:3001/graphql`

### Query

Now we can make a `hello` query to the `graphql` server as follows:

```shell
query Hello {
  hello
}

```

We will get the following response from the `server`

```json
{
  "data": {
    "hello": "hello world"
  }
}
```

### Uploading Files

Next we are going to show how we can upload a file using `cURL`. We are going to use upload an image named `cover.jpg` to the server. We are going to run the following mutation.

```shell
curl http://127.0.0.1:3001/graphql/  -F operations='{ "query": "mutation UploadFile($file: Upload!){ uploadFile(file: $file){ success } }", "variables": { "file": null } }'  -F map='{ "0": ["variables.file"] }'  -F 0=@cover.jpg
```

If everything went well we are going to get the following response from the server:

```json
{
  "data": {
    "uploadFile": {
      "success": true
    }
  }
}
```

### Uploading using Postman

1. Change the request method to `POST`
2. Enter the following `url` in the address bar:
   - `http://localhost:3001/graphql` or `http://127.0.0.1:3001/graphql`
3. Go to the `Body` tab and select `Form Data`
4. Under `operations` key enter the following:

```json
{
  "query": "mutation UploadFile($file: Upload!){ uploadFile(file: $file){ success } }",
  "variables": { "file": null }
}
```

5. Under `map` key enter the following:

```json
{ "0": ["variables.file"] }
```

6. Under `0` key change the type to file and select the file that you want to upload and click send.

If everything went well we are going to get the following response from the server:

```json
{
  "data": {
    "uploadFile": {
      "success": true
    }
  }
}
```

### Uploading Multiple Files

The following is the mutation for uploading multiple files:

```py
class UploadFileMutation(graphene.Mutation):
    class Arguments:
        files = graphene.NonNull(graphene.List(Upload))

    success = graphene.Boolean()

    def mutate(self, info, files, **kwargs):
        print(files)
        return UploadFileMutation(success=True)

class Mutation(graphene.ObjectType):
    uploadFile = UploadFileMutation.Field()
```

Using cURL

```shell
curl http://localhost:3001/graphql/  -F operations='{ "query": "mutation UploadFile($files: [Upload]!){ uploadFile(files: $files){ success } }", "variables": { "files":[ null, null ] } }' -F map='{ "0": ["variables.files.0"], "1": ["variables.files.1"] }' -F 0=@README.md -F 1=@LICENSE
```

Using Postman

![img](https://i.stack.imgur.com/fhTKf.png)

> image taken from [here](https://stackoverflow.com/questions/61488358/uploading-files-via-graphql-setting-up-server-and-client-sides-and-querying-via)

### Serving Static Files

In this section I will show how we can server static files to the browser over a `url`. First we need to open the `file_uploads/file_uploads/urls.py` and add the `static` url to our `urlpatterns` as follows:

```py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import os

# The folder where we want to serve the static file from
PATH = os.path.join(os.getcwd(), "images")

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'graphql/', include('api.urls'))
]  + static('/images', document_root=PATH)
```

So the `static` function takes in the first argument as the path and the second argument as an absolute directory to where the files and folders that we are exposing. In our case we are exposing the `images` folder. Now with this we can be able to access the `cover.jpg` by visiting `http://127.0.0.1/images/cover.jpg`

### Refs

1.[stackoverflow.com](https://stackoverflow.com/questions/61892306/is-there-any-way-to-upload-files-via-postman-into-a-graphql-api)

2. [frankmeszaros.medium.com](https://frankmeszaros.medium.com/end-to-end-file-upload-with-react-django-and-graphql-710a44cae153)

3. [00_GRAPHENE_BASICS - github](https://github.com/CrispenGari/python-and-django/tree/main/02_GRAPHQL_APIS/00_GRAPHENE_BASICS)

4. [github.com/CrispenGari](https://github.com/CrispenGari/WAC/blob/main/server/api/blueprints/__init__.py)

5. [docs.djangoproject.com](https://docs.djangoproject.com/en/2.1/ref/urls/#static)

6. [stackoverflow.com](https://stackoverflow.com/questions/40248356/how-to-serve-a-directory-of-static-files-at-a-custom-url-in-django)
