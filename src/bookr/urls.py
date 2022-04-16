from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import site
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import include
from django.urls import path

from bookr.views import profile


urlpatterns: list[URLPattern | URLResolver] = [
    path("book_management/", include("book_management.urls")),
    path(
        "accounts/",
        include(("django.contrib.auth.urls", "auth"), namespace="accounts"),
    ),
    path("accounts/profile/", profile, name="profile"),
    path("admin/", site.urls),
    path("", include("reviews.urls")),
]
if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
