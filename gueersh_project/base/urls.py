from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('music/', views.music, name='music'),
    
    path('band/<int:band_id>/', views.show_band, name='show_band'),
    path('create_band/', views.create_band, name='create_band'),
    path('band/<int:band_id>/add-social/', views.add_social_network, name='add_social_network'),
    
    path('release/<int:release_id>/', views.show_release, name='show_release'),
    path('create_release/', views.create_release, name='create_release'),
    
    path('profile/<str:username>/', views.show_profile, name='show_profile'),
    
    path('posts/<int:post_id>/', views.show_post, name='show_post'),
    path('create_post/', views.create_post, name='create_post'),
]