from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler403
from . import handlers


handler404 = handlers.handler404
handler403 = handlers.handler403
handler500 = handlers.handler500


urlpatterns = [
    path("cp-7x9a2b7f3e1d8c5b4/", admin.site.urls),
    path("", include("home.urls")),
    path("account/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
    path("summernote/", include("django_summernote.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
