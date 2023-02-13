from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group")
        help_text = {
            'text': 'Текст',
            'group': 'Группа',
        }
        labels = {
            'text': 'Текст',
            'group': 'Группа',
        }

    def clean_subject(self):
        data = self.cleaned_data['text']
        if '' not in data():
            raise forms.ValidationError(
                'Поле не может быть пустым'
            )
        return data
