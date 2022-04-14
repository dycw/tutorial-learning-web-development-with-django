from django.urls import path

from reviews.views import welcome_view


urlpatterns = [path("", welcome_view, name="welcome_view")]
