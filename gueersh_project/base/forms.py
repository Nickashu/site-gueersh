from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Band, BandSocialNetwork, Release


# Formulário para o model Post:
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'main_image', 'main_description', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name', 'description', 'image', 'video_link', 'spotify_link']



class BandSocialNetworkForm(forms.ModelForm):
    class Meta:
        model = BandSocialNetwork
        fields = ['social_network', 'link']
        widgets = {
            'link': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['link'].required = True




class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        fields = ['band', 'title', 'image', 'release_date', 'description', 'video_link', 'spotify_link']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        
        def clean(self):
            cleaned_data = super().clean()
            image = cleaned_data.get('image')
            if not image:
                self.add_error('image', 'Você deve enviar uma imagem para o lançamento.')

            return cleaned_data
