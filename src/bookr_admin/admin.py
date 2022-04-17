from itertools import chain
from typing import Any

from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from django.urls import URLResolver
from django.urls.resolvers import URLPattern


class BookrAdmin(AdminSite):
    site_header = "Bookr Administration"

    def profile_view(self, request: Any) -> TemplateResponse:
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

    def get_urls(self) -> list[URLResolver | URLPattern]:  # type: ignore
        return list(
            chain(
                super().get_urls(),
                [path("admin_profile", self.admin_view(self.profile_view))],
            )
        )
