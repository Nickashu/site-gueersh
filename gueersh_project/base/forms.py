from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Band, BandSocialNetwork, Release, NewsletterSubscriber, ReleaseCredits, Contact, Tour, Concert
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['name'].widget.attrs.update({'placeholder': 'Nome da banda'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Descrição da banda'})
        self.fields['video_link'].widget.attrs.update({'placeholder': 'https://...'})
        self.fields['spotify_link'].widget.attrs.update({'placeholder': 'https://...'})



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
            'release_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['title'].widget.attrs.update({'placeholder': 'Título do lançamento'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Descrição do lançamento'})
        self.fields['video_link'].widget.attrs.update({'placeholder': 'https://...'})
        self.fields['spotify_link'].widget.attrs.update({'placeholder': 'https://...'})


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu e-mail...'
            })
        }
        
class ReleaseCreditsForm(forms.ModelForm):
    class Meta:
        model = ReleaseCredits
        fields = ['role', 'crew']
        widgets = {
            'role': forms.TextInput(attrs={'placeholder': 'Ex: Produção, Mixagem...'}),
            'crew': forms.Textarea(attrs={'placeholder': 'Equipe responsável'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['role', 'name', 'email']
        widgets = {
            'role': forms.TextInput(attrs={'placeholder': 'Cargo'}),
            'name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        }
        
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['year']
        widgets = {
            'year': forms.NumberInput(attrs={'placeholder': 'Ano da turnê'}),
        }

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['date', 'city', 'state', 'country', 'venue']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Data do show'}, format='%Y-%m-%d'),
            'city': forms.TextInput(attrs={'placeholder': '"Cidade onde o show ocorrerá. Ex: São Paulo"'}),
            'state': forms.TextInput(attrs={'placeholder': 'Estado onde o show ocorrerá (opcional). Ex: SP'}),
            'country': forms.TextInput(attrs={'placeholder': 'País onde o show ocorrerá. Ex: Brasil'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Local onde o show ocorrerá. Ex: Circo Voador'}),
        }

#Sobrescrevendo o formulário para o registro de usuários:
User = get_user_model()
class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Já existe uma conta com este endereço de e-mail.")
        return email

