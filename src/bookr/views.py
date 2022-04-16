from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "profile.html")
