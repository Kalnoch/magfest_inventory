from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils.timezone import now
from django.db.models import F, Count
from django.core.exceptions import ObjectDoesNotExist
from .tournaments import Tournaments

from .models import Item, Tournament, TournamentPlayer
from inventory.reggie_interface import ReggieInterface

from random import shuffle


# Create your views here.
def index(request):
    item_list = Item.objects.order_by('barcode')[:10]
    output = ', '.join([i.name for i in item_list])
    context = {'item_list': item_list}
    return HttpResponse(output)


def available(request):
    item_list = Item.objects.filter(checked_out=False).order_by('barcode')[:10]
    output = ', '.join([i.name for i in item_list])
    context = {'item_list': item_list}
    return HttpResponse(output)


def checkedout(request):
    item_list = Item.objects.filter(checked_out=True).order_by('barcode')[:10]
    output = ', '.join([i.name for i in item_list])
    context = {'item_list': item_list}
    return HttpResponse(output)


def games_index(request):
    games_list = Item.objects.filter(type='Game').order_by('name')
    output = '\n'.join([g.name for g in games_list])
    context = {'item_list': games_list}
    return HttpResponse(output)


def games_available(request):
    games_list = Item.objects.filter(type='Game', checked_out=False).order_by('name')
    output = '\n'.join([g.name for g in games_list])
    context = {'item_list': games_list}
    return HttpResponse(output)


def games_checked_out(request):
    games_list = Item.objects.filter(type='Game', checked_out=True).order_by('name')
    output = '\n'.join([g.name for g in games_list])
    context = {'item_list': games_list}
    return HttpResponse(output)


# def checkout(request):
#
#     return HttpResponse(output)


def tournament_main_page(request):
    return render(request, 'inventory/tournament_main_page.html')


def tournament_index(request):
    tournament_list = Tournament.objects.order_by('start_time')
    template = loader.get_template('inventory/tournaments_index.html')
    context = {'tournament_list': tournament_list}
    return HttpResponse(template.render(context, request))


def open_tournament(request):
    tournament_list = Tournament.objects.annotate(count=Count('players')).filter(open_time__lte=now(), start_time__gt=now()).exclude(max_players=F('count')).order_by('start_time')
    return render(request, 'inventory/tournaments_index.html', {'tournament_list': tournament_list})


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return render(request, 'inventory/tournament_detail.html', {'tournament': tournament})


def tournament_signup(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    t = Tournaments()
    tournament_list = Tournament.objects.filter(open_time__lte=now(), start_time__gt=now()).order_by('start_time')
    if t.sign_up(tournament, request.POST['barcode']):
        return render(request, 'inventory/tournament_detail.html', {'tournament': tournament,
                                                                   'error_message': "You have successfully signed up"})
        # return render(request, 'inventory/tournaments_index.html', {'tournament_list': tournament_list})
    return render(request, 'inventory/tournament_detail.html', {'tournament': tournament,
                                                                'error_message': "Signup unsuccessful, sorry, it might be full"})


def tournament_player_list(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    player_list = tournament.players.all()
    return render(request, 'inventory/tournament_players.html', {'tournament': tournament,
                                                                 'players_list': player_list})


def tournament_player_list_shuffled(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    player_list = list(tournament.players.all())
    shuffle(player_list)
    return render(request, 'inventory/tournament_players.html', {'tournament': tournament,
                                                                 'players_list': player_list})


def player_info(request):
    return render(request, 'inventory/player.html')


def get_player_detail(request):
    reggie = ReggieInterface()
    r = reggie.lookup_attendee_from_barcode(request.POST['barcode'])
    if r is not None:
        try:
            player = TournamentPlayer.objects.get(badge_number=r['result']['badge_num'])
            tournament_list = Tournament.objects.filter(players__id=player.id)

            return render(request, 'inventory/player_detail.html', {'player': player,
                                                                    'tournament_list': tournament_list})
        except ObjectDoesNotExist:
            pass
    return render(request, 'inventory/player_detail.html')
