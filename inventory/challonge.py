import challonge
import json

from inventory_system.settings import CHALLONGE_AUTH_TOKEN

challonge.set_credentials('Kalnoch', CHALLONGE_AUTH_TOKEN)


def create_tournament(tournament):
    return challonge.tournaments.create(
        tournament.name,
        # "",
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


def check_in_player(tournament, player):
    player_id = json.loads(player.challonge_ids)[str(tournament.challonge_id)]
    challonge.participants.check_in(tournament.challonge_id, player_id)
