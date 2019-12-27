from inventory.reggie_interface import ReggieInterface
from inventory.models import TournamentPlayer
from django.utils.timezone import now


class Tournaments:

    def __init__(self):
        self.reggie = ReggieInterface()

    def sign_up(self, tournament, barcode):
        # Takes a barcode and signs up the given player
        r = self.reggie.lookup_attendee_from_barcode(barcode)
        if r is not None:
            player, created = TournamentPlayer.objects.get_or_create(first_name=r['result']['first_name'],
                                                                     last_name=r['result']['last_name'],
                                                                     badge_number=r['result']['badge_num'])

            if tournament.players.count() < tournament.max_players and now() > tournament.open_time:
                tournament.players.add(player)
                return True
            else:
                return False

    @staticmethod
    def remove_from_tournament(self, tournament, player):
        # Takes a given tournament and player and removes the player from the tournament
        # Does not throw any errors if the player is not in the tournament
        tournament.players.remove(player)
