from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from .models import Band, Contact, Tour, Concert, BandSocialNetwork, Release, ReleaseCredits, FeitioProfile, Post, SocialNetwork, NewsletterSubscriber
from .forms import PostForm, BandForm, BandSocialNetworkForm, ReleaseForm, NewsletterSubscriberForm
from django.contrib import messages
from django.http import JsonResponse
from allauth.account.models import EmailAddress

logging.basicConfig(level=logging.INFO)

#Páginas principais:
def home(request):
    posts = get_posts()
    context = { 'posts': posts }
    return render(request, 'base/home.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def music(request):
    bands = Band.objects.all()
    last_releases = Release.objects.order_by('created_at')[:2]
    context = {
        'bands': bands,
        'last_releases': last_releases,
    }
    return render(request, 'base/music.html', context)


#Páginas de detalhes:
def show_band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    band_contacts = Contact.objects.filter(band=band)
    band_tours = Tour.objects.filter(band=band)
    tours = []
    for band_tour in band_tours:
        tour = {}
        tour['year'] = band_tour.year
        concerts = []
        for concert in Concert.objects.filter(tour=band_tour).order_by('date'):
            concert_info = {
                'date': f"{concert.date.day}/{concert.date.month}" if concert.date else 'Sem data',
                'city': concert.city if concert.city else '',
                'state': concert.state if concert.state else '',
                'country': concert.country,
                'venue': concert.venue if concert.venue else 'Sem local definido',
            }
            concerts.append(concert_info)
        tour['concerts'] = concerts
        
        tours.append(tour)
    
    social_networks = []
    for band_social_network in BandSocialNetwork.objects.filter(band=band):
        social_network = {}
        social_network['id'] = band_social_network.social_network.id
        social_network['html_icon'] = band_social_network.social_network.html_icon
        social_network['link'] = band_social_network.link
        social_networks.append(social_network)

    context = {
        'band': band,
        'contacts': band_contacts,
        'tours': tours,
        'social_networks': social_networks,
    }
    return render(request, 'base/band/show_band.html', context)


def show_release(request, release_id):
    release = get_object_or_404(Release, id=release_id)
    custom_description = release.description.split('\n')
    release_credits = []
    for release_credit in ReleaseCredits.objects.filter(release=release):
        credit = {}
        credit['role'] = release_credit.role
        credit['crew'] = release_credit.crew.split('\n')
        release_credits.append(credit)
    
    context = {
        'release': release,
        'custom_description': custom_description,
        'release_credits': release_credits,
    }
    return render(request, 'base/release/show_release.html', context)


def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    custom_content = post.content.split('\n')
    context = {
        'post': post,
        'custom_content': custom_content,
    }
    return render(request, 'base/post/show_post.html', context)


@login_required
def show_profile(request, username):
    profile = get_object_or_404(FeitioProfile, user__username=username)
    is_owner = (request.user == profile.user)

    context = {
        'profile': profile,
        'is_owner': is_owner,
    }
    return render(request, 'base/profile/show_profile.html', context)


#Páginas de criação:
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'base/post/create_post.html', {'form': form})


@user_passes_test(is_staff_user)
def create_band(request):
    if request.method == 'POST':
        form = BandForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Banda criada com sucesso.")
            return redirect('home')
    else:
        form = BandForm()

    return render(request, 'base/band/create_band.html', {'form': form})


@login_required
def add_social_network(request, band_id):
    band = get_object_or_404(Band, id=band_id)

    #Precisa ser staff ou membro da banda
    if not request.user.is_staff and request.user.feitio_profile not in band.members.all():
        messages.error(request, "Você não tem permissão para adicionar redes sociais a esta banda.")
        return redirect('show_band', band_id=band.id)

    if request.method == 'POST':
        form = BandSocialNetworkForm(request.POST)
        if form.is_valid():
            band_social = form.save(commit=False)
            band_social.band = band
            band_social.save()
            messages.success(request, "Rede social adicionada com sucesso.")
            return redirect('show_band', band_id=band.id)
    else:
        form = BandSocialNetworkForm()

    return render(request, 'base/band/add_social_network.html', {
        'form': form,
        'band': band
    })

@login_required
def remove_social_network(request, band_id, social_id):
    band = get_object_or_404(Band, id=band_id)
    social = get_object_or_404(SocialNetwork, id=social_id)

    #Precisa ser staff ou membro da banda
    if not request.user.is_staff and request.user.feitio_profile not in band.members.all():
        messages.error(request, "Você não tem permissão para remover redes sociais desta banda.")
        return redirect('show_band', band_id=band.id)

    band_social_network = get_object_or_404(BandSocialNetwork, social_network=social, band=band)
    band_social_network.delete()
    messages.success(request, "Rede social removida com sucesso.")
    return redirect('show_band', band_id=band.id)


@user_passes_test(is_staff_user)
def create_release(request):
    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES)
        if form.is_valid():
            release = form.save()
            messages.success(request, "Lançamento criado com sucesso.")
            return redirect('show_release', release_id=release.id)
    else:
        form = ReleaseForm()

    return render(request, 'base/release/create_release.html', {'form': form})


#Inscrição na newsletter:
def newsletter_subscription(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = NewsletterSubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            #Verifica se o email pertence a um usuário do sistema já cadastrado e verificado:
            if not EmailAddress.objects.filter(email__iexact=email, verified=True).exists():
                return JsonResponse({
                    "status": "danger",
                    "message": "Este e-mail ainda não está cadastrado no sistema ou ainda não foi validado."
                })

            #Verifica se o email informado já está inscrito na newsletter:
            if NewsletterSubscriber.objects.filter(email__iexact=email).exists():
                return JsonResponse({
                    "status": "warning",
                    "message": "Este e-mail já está inscrito na newsletter."
                })

            form.save()
            return JsonResponse({
                "status": "success",
                "message": "E-mail inscrito com sucesso!"
            })

        return JsonResponse({
            "status": "danger",
            "message": "E-mail inválido."
        })

    return JsonResponse({
        "status": "danger",
        "message": "Requisição inválida."
    })


#Métodos auxiliares:
def get_posts():
    return Post.objects.all().order_by('-created_at')