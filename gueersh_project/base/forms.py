from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post


# Formulário para o model Post:
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'main_image', 'main_description', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
