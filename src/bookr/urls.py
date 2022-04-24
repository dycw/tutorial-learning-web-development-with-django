from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import site
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import include
from django.urls import path

from bookr.views import profile
from bookr.views import reading_history
from reviews.views import book_search
from reviews.views import index
from reviews.views import react_example


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "accounts/",
        include(("django.contrib.auth.urls", "auth"), namespace="accounts"),
    ),
    path("accounts/profile/", profile, name=profile.__name__),
    path(
        "accounts/profile/reading_history/",
        reading_history,
        name=reading_history.__name__,
    ),
    path("admin/", site.urls),
    path("", index),
    path("book-search/", book_search, name=book_search.__name__),
    path("", include("reviews.urls")),
    path("react-example/", react_example, name=react_example.__name__),
]
if settings.DEBUG:
    from debug_toolbar import urls

    urlpatterns.append(path("__debug__/", include(urls)))
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
