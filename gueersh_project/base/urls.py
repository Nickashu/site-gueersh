from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('music/', views.music, name='music'),
    #path('<int:pk>/', views.note_detail, name='note_detail'),
    #path('new/', views.note_create, name='note_create'),
    #path('problems/', views.show_problems, name='show_problems'),
    #path('submit_worker_node/', views.submit_worker_node, name='submit_worker_node'),
]