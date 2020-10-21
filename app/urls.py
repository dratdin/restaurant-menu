from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from carts.views import carts_app
from dishes.views import dish_list

urlpatterns = [
    url(r"^$", dish_list, name="index"),
    url(r"^dishes/", include(("dishes.urls", "dishes"), namespace="dishes")),
    url(r"^carts/$", carts_app, name="carts"),
    url(r"^api/carts/", include(("carts.api.urls", "carts_api"), namespace="carts-api")),
    url(r"^admin/", admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
