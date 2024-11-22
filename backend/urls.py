from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings

handler403 = "main.views.tr_handler403"
handler404 = "main.views.tr_handler404"
handler500 = "main.views.tr_handler500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"
    ),
    path("", include("main.urls")),
    path("", include("pwa.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
