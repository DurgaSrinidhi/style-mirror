from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.views import style_mirror_home


urlpatterns = [

    # STYLE MIRROR homepage
    path("", style_mirror_home),

    # Django admin
    path("admin/", admin.site.urls),

    # STYLE MIRROR APIs
    path("api/", include("api.urls")),

]


# Serve uploaded images during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )