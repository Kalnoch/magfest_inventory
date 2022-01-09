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

    @staticmethod
    def determine_m_points(self, tournament):
        # Takes a given tournament and sets the number of m-points
        # Run at print time of tournament?
        payout_1 = (5, 0, 0, 0)
        payout_2 = (5, 3, 1, 0)
        payout_3 = (6, 3, 1, 0)
        payout_4 = (7, 3, 2, 0)
        payout_5 = (8, 4, 2, 0)
        payout_6 = (10, 4, 2, 0)
        payout_7 = (10, 4, 2, 1)
        payout_8 = (15, 5, 3, 1)
        payout_9 = (20, 10, 5, 1)
        m_point_bracket = {4: payout_1,
                           5: payout_1,
                           6: payout_1,
                           7: payout_1,
                           8: payout_2,
                           9: payout_3,
                           10: payout_3,
                           11: payout_3,
                           12: payout_3,
                           13: payout_3,
                           14: payout_3,
                           15: payout_3,
                           16: payout_3,
                           17: payout_4,
                           18: payout_4,
                           19: payout_4,
                           20: payout_4,
                           21: payout_4,
                           22: payout_4,
                           23: payout_5,
                           24: payout_5,
                           25: payout_5,
                           26: payout_5,
                           27: payout_6,
                           28: payout_6,
                           29: payout_7,
                           30: payout_8,
                           31: payout_8,
                           32: payout_9
                           }
        smash_pay_1 = (10, 6, 3, 1)
        smash_pay_2 = (15, 6, 3, 1)
        smash_pay_3 = (30, 20, 10, 5)
        smash_bracket = {8: smash_pay_1,
                         24: smash_pay_2,
                         40: smash_pay_3
                         }
        p_count = tournament.players.count()
        if tournament.name.startswith("Smash"):
            if p_count > 40:
                return smash_pay_3
            elif p_count > 24:
                return smash_pay_2
            elif p_count > 8:
                return smash_pay_1
            else:
                return 0
        else:
            if p_count in m_point_bracket:
                m_points = m_point_bracket[p_count]
                return m_points
            else:
                return 0
