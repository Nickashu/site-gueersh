from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('music/', views.music, name='music'),
    
    path('group/<int:band_id>/', views.show_band, name='show_band'),
    path('release/<int:release_id>/', views.show_release, name='show_release'),
    
    path('profile/<str:username>/', views.show_profile, name='show_profile'),
    
    path('posts/<int:post_id>/', views.show_post, name='show_post'),
    path('create_post/', views.create_post, name='create_post'),
]