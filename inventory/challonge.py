import challonge
import json

from inventory_system.settings import CHALLONGE_AUTH_TOKEN

challonge.set_credentials('Kalnoch', CHALLONGE_AUTH_TOKEN)


def create_tournament(tournament):
    return challonge.tournaments.create(
        tournament.name,
        f"mag2024_{tournament.id}",
        organization_id=161390,
        open_signup=False,
        private=True,
        signup_cap=tournament.max_players,
        start_at=tournament.start_time,
        check_in_duration=15,
    )


def update_tournament(tournament, **kwargs):
    challonge.tournaments.update(
        tournament.challonge_id,
        signup_cap=tournament.max_players,
        start_at=tournament.start_time,
        **kwargs
    )


def signup_player(tournament, player):
    participant = challonge.participants.create(
        tournament.challonge_id,
        " ".join([player.first_name, player.last_name]),
    )
    challonge_ids = json.loads(player.challonge_ids)
    challonge_ids[tournament.challonge_id] = participant['id']
    player.challonge_ids = json.dumps(challonge_ids)
    player.save()


def signup_team(tournament, players):
    team_name = "/".join([player.first_name for player in players])
    participant = challonge.participants.create(
        tournament.challonge_id,
        team_name,
    )
    for player in players:
        challonge_ids = json.loads(player.challonge_ids)
        challonge_ids[tournament.challonge_id] = participant['id']
        player.challonge_ids = json.dumps(challonge_ids)
        player.save()


def check_in_player(tournament, player):
    player_id = json.loads(player.challonge_ids)[str(tournament.challonge_id)]
    challonge.participants.check_in(tournament.challonge_id, player_id)


def remove_player(tournament, player):
    tournament_id = str(tournament.challonge_id)
    challonge_ids = json.loads(player.challonge_ids)
    try:
        challonge.participants.destroy(tournament_id, challonge_ids[tournament_id])
    except:  # TODO: catch the HTTP 404 error correctly and handle
        pass
    challonge_ids.pop(tournament_id)
    player.challonge_ids = json.dumps(challonge_ids)
    player.save()
