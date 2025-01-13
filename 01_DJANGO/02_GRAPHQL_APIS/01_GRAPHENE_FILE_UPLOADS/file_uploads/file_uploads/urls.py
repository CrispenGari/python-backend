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