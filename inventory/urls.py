from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('checkout', views.checkout, name='checkout'),
    path('available', views.available, name='available'),
    path('checkedout', views.checkedout, name='checked out'),
    path('games/', views.games_index, name='games'),
    path('tournaments/', views.tournament_index, name='tournaments'),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament detail'),
    path('tournaments/<int:tournament_id>/signup', views.tournament_signup, name='tournament signup'),
]
