from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from form_example.forms import ExampleForm


def form_example(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if (form := ExampleForm(request.POST)).is_valid():
            for key, value in form.cleaned_data.items():
                print(f"{key}, {type(value)}, {value}")
    else:
        form = ExampleForm()
    return render(
        request, "form-example.html", {"method": request.method, "form": form}
    )
