from typing import Any
from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from plotly.graph_objects import Figure
from plotly.graph_objects import Scatter
from plotly.offline import plot

from reviews.utils import get_books_read_by_month


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    user = cast(Any, request.user)
    permissions = user.get_all_permissions()
    # Get the books read in different months this year
    books_read_by_month = get_books_read_by_month(user.username)

    # Initialize the Axis for graphs, X-Axis is months, Y-axis is books read
    months = [i + 1 for i in range(12)]
    books_read = [0 for _ in range(12)]

    # Set the value for books read per month on Y-Axis
    for num_books_read in books_read_by_month:
        list_index = num_books_read["date_created__month"] - 1
        books_read[list_index] = num_books_read["book_count"]

    # Generate a scatter plot HTML
    figure = Figure()
    scatter = Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Month", yaxis_title="No. of books read")
    plot_html = plot(figure, output_type="div")

    return render(
        request,
        "profile.html",
        {
            "user": user,
            "permissions": permissions,
            "books_read_plot": plot_html,
        },
    )
