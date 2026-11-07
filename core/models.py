from django.db import models
from django.conf import settings


class Fixture(models.Model):
    api_id = models.IntegerField(unique=True)

    league_name = models.CharField(max_length=100)

    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)

    fixture_date = models.DateTimeField()

    status = models.CharField(max_length=10)

    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"[{self.league_name}] "
            f"{self.home_team} {self.home_score}:{self.away_score} "
            f"{self.away_team} ({self.status})"
        )

class News(models.Model):
    news_id = models.CharField(
        max_length=100,
        unique=True
    )

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=100)
    article_url = models.URLField()
    image_url = models.URLField(blank=True)
    sport = models.CharField(
        max_length=50,
        default="Football"
    )

    published_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Posts(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Posts"
        verbose_name_plural = "Posts"


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="news_comments"
    )
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Коментар {self.author} до «{self.news.title}»"