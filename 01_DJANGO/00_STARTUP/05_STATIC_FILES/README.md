### Static Files and Loading Bootstrap

In this section we are going to have a look on how we can load static files in template using django. Just like what we did with templates we need to create a folder called `static` and inside the static we are going to have a sub directory called `blog`. To group our static files we are going to create sub directories in the `/static/blog` folder for all the static files, so that images will be grouped in their directory, css files in their directory, etc. The folder structure will be looking as follows:

```
📁 05_STATIC_FILES
    📁 orm_databases
        📁 blog
            📁 __pycache__
            📁 migrations
        📁 templates
        📁 static
             📁 blog
                 📁 css
                 📁 js
                 📁 images
```

### Loading static files in templates

To load static files in template first we go to our `base.html` and at the top of the file we add the `{% load static %}`. This tells the template engine that we are going to load static files in this template.

```html
<!-- base.html -->
{% load static %}
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

> Note that in each and every file that we need to load a static file we put the `{% load static %}` at the top.

1. loading css

To load `css` files in our template we do it as follows

```html
<link
  rel="stylesheet"
  type="text/css"
  href="{% static 'blog/css/index.css' %}"
/>
```

2. loading js

To load `js` files in our templates we do it as follows:

```html
<script src="{% static 'blog/js/index.js' %}"></script>
```

3. loading images

To load `image` files to our templates we do it as follows:

```html
<img src="{% static 'blog/images/1.jpg' %}" alt="image" />
```

### Bootstrap

To add bootstrap we are going to make use of CDN's so we go to [Bootstrap documentation](https://getbootstrap.com/docs/4.6/getting-started/introduction/) and copy and paste the cdn's in the base.html file. We load both the javascript, jquery and css:

1. javascript cdn's

These cdn's must be just before the closing `body` tag

```html
<script
  src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
  integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
  crossorigin="anonymous"
></script>
<script
  src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"
  integrity="sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF"
  crossorigin="anonymous"
></script>
```

2. css cdn's

These cdn's must be in the `head` tag of the html document

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
  integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
  crossorigin="anonymous"
/>
```

The `base.html` file will then looks as follows:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
      integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
      crossorigin="anonymous"
    />
    <link
      rel="stylesheet"
      type="text/css"
      href="{% static 'blog/css/index.css' %}"
    />
    {% block title %} {% endblock title %}
  </head>
  <body>
    {% block content %} {% endblock content %}
    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    <script
      src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
      integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF"
      crossorigin="anonymous"
    ></script>
    <script src="{% static 'blog/js/index.js' %}"></script>
  </body>
</html>
```

### Next

In the next section we are going to have a look at how we can create a user registration form.

### Ref

1. [Bootstrap 4](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
