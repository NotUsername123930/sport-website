from django.shortcuts import render
from .models import Fixture  # Імпортуємо нашу модель матчів


def home_page(request):
    # Дістаємо абсолютно всі матчі, які ми успішно зберегли в базу даних
    matches_list = Fixture.objects.all()

    # Готуємо "контекст" — словник із даними, які ми передаємо у фронтенд
    context = {
        "matches": matches_list
    }

    # Відправляємо користувачу твій фінальний HTML-макет разом із цими матчами
    return render(request, "index.html", context)