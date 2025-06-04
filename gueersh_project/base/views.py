from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Band, Contact, Tour, Concert, BandSocialNetwork, Release, ReleaseCredits, FeitioProfile, Post
from django.contrib.auth.decorators import user_passes_test
from .forms import PostForm

logging.basicConfig(level=logging.INFO)

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
        social_network['html_icon'] = band_social_network.social_network.html_icon
        social_network['link'] = band_social_network.link
        social_networks.append(social_network)

    context = {
        'band': band,
        'contacts': band_contacts,
        'tours': tours,
        'social_networks': social_networks,
    }
    return render(request, 'base/show_band.html', context)


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
    return render(request, 'base/show_release.html', context)


@login_required
def show_profile(request, username):
    profile = get_object_or_404(FeitioProfile, user__username=username)
    is_owner = (request.user == profile.user)

    context = {
        'profile': profile,
        'is_owner': is_owner,
    }
    return render(request, 'base/show_profile.html', context)




#Posts:
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
    
    return render(request, 'base/posts/create_post.html', {'form': form})


def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    custom_content = post.content.split('\n')
    context = {
        'post': post,
        'custom_content': custom_content,
    }
    return render(request, 'base/posts/show_post.html', context)





#Métodos auxiliares:

def get_posts():
    return Post.objects.all().order_by('-created_at')