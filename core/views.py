from collections import defaultdict
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CommentForm
from .models import Comment, Fixture, News, Posts


def home_page(request):

    selected_league = request.GET.get("league")

    selected_date = request.GET.get("date")

    if not selected_date:
        selected_date = str(date.today())

    current_date = date.fromisoformat(selected_date)

    previous_day = current_date - timedelta(days=1)
    next_day = current_date + timedelta(days=1)

    live_matches = Fixture.objects.exclude(
        status__in=["NS", "FT"]
    ).order_by("fixture_date")

    upcoming_matches = Fixture.objects.filter(
        status="NS"
    ).order_by("fixture_date")

    finished_matches = Fixture.objects.filter(
        status="FT"
    ).order_by("-fixture_date")

    daily_matches = Fixture.objects.filter(
        fixture_date__date=selected_date
    ).order_by("fixture_date")

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

        daily_matches = daily_matches.filter(
            league_name=selected_league
        )

    leagues = (
        Fixture.objects
        .values_list("league_name", flat=True)
        .distinct()
    )

    latest_news = News.objects.order_by(
        "-published_at"
    )[:10]

    latest_post = Posts.objects.filter(
        is_published=True
    ).order_by("-created_at").first()

    calendar = defaultdict(list)

    for match in Fixture.objects.order_by("fixture_date"):
        calendar[match.fixture_date.date()].append(match)

    context = {
        "live_matches": live_matches,
        "upcoming_matches": upcoming_matches,
        "finished_matches": finished_matches,
        "daily_matches": daily_matches,

        "live_count": live_matches.count(),
        "upcoming_count": upcoming_matches.count(),
        "finished_count": finished_matches.count(),

        "latest_news": latest_news,

        "leagues": leagues,
        "selected_league": selected_league,

        "latest_post": latest_post,

        "calendar": dict(calendar),

        "selected_date": selected_date,
        "previous_day": previous_day,
        "next_day": next_day,
    }

    return render(request, "index.html", context)


def league_page(request, league_name):

    matches = Fixture.objects.filter(
        league_name=league_name
    ).order_by("fixture_date")

    context = {
        "league_name": league_name,
        "matches": matches,
    }

    return render(
        request,
        "league.html",
        context
    )


def news_page(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = (
        Comment.objects
        .filter(news=news)
        .select_related("author")
    )

    return render(request, "news.html", {
        "news": news,
        "comments": comments,
        "comment_form": CommentForm(),
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {
        "form": form,
    })


@login_required
@require_POST
def post_comment(request, news_id):
    news = get_object_or_404(News, id=news_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.news = news
        comment.author = request.user
        comment.save()
        messages.success(request, "Коментар додано.")
    else:
        messages.error(request, "Напиши коментар перед відправленням.")

    return redirect(
        reverse("news_page", args=[news.id]) + "#comments"
    )

