from django.urls import include
from django.urls import path

from reviews.admin import site


urlpatterns = [path("admin/", site.urls), path("", include("reviews.urls"))]
