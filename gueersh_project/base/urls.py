from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('music/', views.music, name='music'),
    
    path('band/<int:band_id>/', views.show_band, name='show_band'),
    path('create_band/', views.create_band, name='create_band'),
    path('band/<int:band_id>/editar/', views.edit_band, name='edit_band'),
    path('band/<int:band_id>/excluir/', views.delete_band, name='delete_band'),
    
    path('band/<int:band_id>/add-social/', views.add_social_network, name='add_social_network'),
    path('band/<int:band_id>/remove-social/<int:social_id>', views.remove_social_network, name='remove_social_network'),
    
    path('release/<int:release_id>/', views.show_release, name='show_release'),
    path('create_release/', views.create_release, name='create_release'),
    path('release/<int:release_id>/editar/', views.edit_release, name='edit_release'),
    path('release/<int:release_id>/excluir/', views.delete_release, name='delete_release'),
    
    path('profile/<str:username>/', views.show_profile, name='show_profile'),
    
    path('posts/<int:post_id>/', views.show_post, name='show_post'),
    path('posts/<int:post_id>/editar/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/excluir/', views.delete_post, name='delete_post'),
    path('create_post/', views.create_post, name='create_post'),
    
    path("newsletter/subscribe/", views.newsletter_subscription, name='newsletter_subscription'),
    path('newsletter/unsubscribe/<uuid:token>/', views.newsletter_unsubscription, name='newsletter_unsubscription'),

]