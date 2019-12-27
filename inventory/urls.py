from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournament_main_page, name='index'),
    # path('checkout', views.checkout, name='checkout'),
    # path('available', views.available, name='available'),
    # path('checkedout', views.checkedout, name='checked out'),
    # path('games/', views.games_index, name='games'),
    path('tournaments/', views.open_tournament, name='open tournaments'),
    path('tournaments/all', views.tournament_index, name='tournaments'),
    path('player_info', views.player_info, name='player info'),
    path('player_detail', views.get_player_detail, name='player detail'),
    path('player_detail/remove', views.remove_player_from_tournament),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament detail'),
    path('tournaments/<int:tournament_id>/signup', views.tournament_signup, name='tournament signup'),
    path('tournaments/<int:tournament_id>/player_list/', views.tournament_player_list, name='tournament players'),
    path('tournaments/<int:tournament_id>/player_list/shuffle', views.tournament_player_list_shuffled, name='shuffled tournament players'),
]


