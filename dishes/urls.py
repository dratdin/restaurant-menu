from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from .views import (
    dish_detail,
    dish_list
    )

urlpatterns = [
    url(r'^category/(?P<category_slug>[^/]+)', dish_list, name='list'),
    url(r'^(?P<slug>[^/]+)', dish_detail, name='detail')
]
