from django.shortcuts import render
from .models import Fixture


def home_page(request):

    matches_list = Fixture.objects.order_by("fixture_date")

    context = {
        "matches": matches_list
    }

    return render(request, "index.html", context)