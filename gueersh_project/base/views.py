from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Band, Contact, Tour, Concert, BandSocialNetwork, BandFeitioProfile

logging.basicConfig(level=logging.INFO)

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def music(request):
    bands = Band.objects.all()
    context = {'bands': bands}
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