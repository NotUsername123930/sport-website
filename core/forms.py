from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": "Коментар",
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 2000,
                "placeholder": "Напиши свій коментар...",
            }),
        }