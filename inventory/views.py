from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils.timezone import now
from django.db.models import F, Count
from django.db.transaction import set_autocommit, commit, rollback
from django.core.exceptions import ObjectDoesNotExist
from random import choice
from .tournaments import Tournaments

from .models import Item, Tournament, TournamentPlayer
from inventory.reggie_interface import ReggieInterface

from random import shuffle


def generate_shakespearean_insult():
    one = ['artless', 'bawdy', 'beslubbering', 'bootless', 'churlish', 'cockered', 'clouted', 'craven', 'currish', 'dankish' ,'dissembling', 'droning', 'errant', 'fawning', 'fobbing', 'froward', 'frothy', 'gleeking', 'goatish', 'gorbellied', 'impertinent', 'infectious', 'jarring', 'loggerheaded', 'lumpish', 'mammering', 'mangled']
    two = ['base-court', 'bat-fowling', 'beef-witted', 'beetle-headed', 'boil-brained', 'clapper-clawed', 'clay-brained', 'common-kissing', 'crook-pated', 'dismal-dreaming', 'dizzy-eyed', 'doghearted', 'dread-bolted', 'earth-vexing', 'elf-skinned', 'fat-kidneyed', 'fen-sucked', 'flap-mouthed', 'fly-bitten', 'folly-fallen', 'fool-born', 'full-gorged', 'guts-griping', 'half-faced', 'hasty-witted', 'hedge-born', 'hell-hated']
    three = ['apple-john', 'baggage', 'barnacle', 'bladder', 'boar-pig', 'bugbear', 'bum-bailey', 'canker-blossom', 'clack-dish', 'clotpole', 'coxcomb', 'codpiece', 'death-token', 'dewberry', 'flap-dragon', 'flax-wench', 'flirt-gill', 'foot-licker', 'fustilarian', 'giglet', 'gudgeon', 'haggard', 'harpy', 'hedge-pig', 'horn-beast', 'hugger-mugger', 'joithead']

    return " ".join(["Thou", choice(one), choice(two), choice(three)])


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
    template = loader.get_template('inventory/tournaments_index_all.html')
    context = {'tournament_list': tournament_list}
    return HttpResponse(template.render(context, request))


def open_tournament(request):
    tournament_list = Tournament.objects.annotate(count=Count('players')).filter(open_time__lte=now(), start_time__gt=now(), printed=False).exclude(max_players=F('count')).exclude(info_only_tournament=True).order_by('start_time')
    tournament_info_list = Tournament.objects.filter(open_time__lte=now(), start_time__gt=now()).exclude(info_only_tournament=False).order_by('start_time')
    return render(request, 'inventory/tournaments_index.html', {'tournament_list': tournament_list,
                                                                'tournament_info_list': tournament_info_list})


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    return render(request, 'inventory/tournament_detail.html', {'tournament': tournament})


def tournament_team_signup(request, tournament, t):
    success = True
    error_messages = ["There was an error in signing up your team:"]
    barcodes = []
    unique_barcodes = set()
    for n in range(tournament.team_size):
        barcode = request.POST[f"barcode{n}"]
        barcodes.append(barcode)
        unique_barcodes.add(barcode)
    if len(unique_barcodes) != tournament.team_size:
        error_messages.append(f"There must be {tournament.team_size} unique players per team")
        return False, error_messages
    success, messages = t.team_sign_up(tournament, barcodes)
    error_messages.extend(messages)
    if success:
        commit()
        return success, [f"All players signed up successfully for {tournament.name}"]
    rollback()
    return success, error_messages


def tournament_signup(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    t = Tournaments()
    message = ""
    message_array = []
    #tournament_list = Tournament.objects.filter(open_time__lte=now(), start_time__gt=now()).order_by('start_time')
    if tournament.team_size > 1:
        set_autocommit(False)
        _, message_array = tournament_team_signup(request, tournament, t)
        set_autocommit(True)
    else:
        _, message = t.single_sign_up(tournament, request.POST['barcode'])
        # return render(request, 'inventory/tournaments_index.html', {'tournament_list': tournament_list})
    return render(request, 'inventory/tournament_signup.html', {'tournament': tournament,
                                                                'error_message': message,
                                                                'error_message_array': message_array})


def runner_index(request):
    tournament_list = Tournament.objects.order_by('start_time')
    department = request.GET.get("department")
    if department:
        tournament_list = tournament_list.filter(department=department)
    return render(request, 'inventory/tournament_runners.html', {'tournament_list': tournament_list})


def runner_detail(request, tournament_id):
    player_teams = []
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not tournament.custom_m_points:
        tournament.m_points = Tournaments.determine_m_points(Tournaments, tournament)
    player_list = tournament.players.all()
    if tournament.team_size > 1:
        player_teams = tournament.tournamentteam_set.all()
    return render(request, 'inventory/runner_detail.html', {'tournament': tournament,
                                                            'players_list': player_list,
                                                            'player_teams': player_teams})


def runner_print(request, tournament_id):
    player_list = None
    player_teams = []
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not tournament.custom_m_points:
        tournament.m_points = Tournaments.determine_m_points(Tournaments, tournament)
    tournament.printed = True
    tournament.save()
    if tournament.team_size == 1:
        player_list = list(tournament.players.all())
        shuffle(player_list)
    else:
        player_teams = list(tournament.tournamentteam_set.all())
        shuffle(player_teams)
    return render(request, 'inventory/runner_print.html', {'tournament': tournament,
                                                           'players_list': player_list,
                                                           'player_teams': player_teams})


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


def remove_player_from_tournament(request):
    player = TournamentPlayer.objects.get(id=request.POST['player'])
    tournament = Tournament.objects.get(id=request.POST['tournament'])
    Tournaments.remove_from_tournament(Tournaments, tournament, player)
    tournament_list = Tournament.objects.filter(players__id=player.id)
    return render(request, 'inventory/player_detail.html', {'player': player,
                                                            'tournament_list': tournament_list})
