from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from dishes.views import dish_list

urlpatterns = [
    url(r'^$', dish_list, name="index"),
    url(r'^dishes/', include('dishes.urls', namespace='dishes')),
    url(r'^carts/', include('carts.urls', namespace='carts')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
