from django.contrib import admin
from .models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published')

    list_filter = ('is_published', 'created_at')

    search_fields = ('title', 'description')

    readonly_fields = ('created_at',)

    list_editable = ('is_published',)

    ordering = ('-created_at',)