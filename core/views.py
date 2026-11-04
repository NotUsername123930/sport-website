from django.shortcuts import render
from .models import Fixture, News


def home_page(request):
    selected_league = request.GET.get("league")


    live_matches = Fixture.objects.exclude(
        status__in=["NS", "FT"]
    ).order_by("fixture_date")

    upcoming_matches = Fixture.objects.filter(
        status="NS"
    ).order_by("fixture_date")

    finished_matches = Fixture.objects.filter(
        status="FT"
    ).order_by("-fixture_date")

    latest_news = News.objects.order_by(
        "-published_at"
    )[:10]

    if selected_league:
        upcoming_matches = upcoming_matches.filter(
            league_name=selected_league
        )

        live_matches = live_matches.filter(
            league_name=selected_league
        )

        finished_matches = finished_matches.filter(
            league_name=selected_league
        )

    leagues = (
        Fixture.objects
        .values_list("league_name", flat=True)
        .distinct()
    )

    context = {
        "live_matches": live_matches,
        "upcoming_matches": upcoming_matches,
        "finished_matches": finished_matches,

        "live_count": live_matches.count(),
        "upcoming_count": upcoming_matches.count(),
        "finished_count": finished_matches.count(),

        "latest_news": latest_news,

        "leagues": leagues,
        "selected_league": selected_league,
    }
    return render(request, "index.html", context)

def league_page(request, league_name):
    matches = Fixture.objects.filter(
        league_name=league_name).order_by("fixture_date")

    context = {
        "league_name": league_name,
        "matches": matches,
    }

    return render(request,"league.html",context)

