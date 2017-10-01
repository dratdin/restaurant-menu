from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from dishes.views import dish_list
from carts.views import (
    carts_app,
)

urlpatterns = [
    url(r'^$', dish_list, name="index"),
    url(r'^dishes/', include("dishes.urls", namespace='dishes')),
    url(r'^carts/$', carts_app, name="crarts"),
    url(r'^api/carts/', include("carts.api.urls", namespace='carts-api')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
