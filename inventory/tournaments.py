from django.utils.timezone import now
from inventory.models import TournamentPlayer, TournamentTeam
from inventory.reggie_interface import ReggieInterface
from .challonge import signup_player, remove_player


class Tournaments:

    def __init__(self):
        self.reggie = ReggieInterface()

    def get_create_tournament_player(self, barcode):
        # Takes a barcode and signs up the given player
        r = self.reggie.lookup_attendee_from_barcode(barcode)
        player = None
        if r is not None:
            player, _ = TournamentPlayer.objects.get_or_create(first_name=r['result']['first_name'],
                                                               last_name=r['result']['last_name'],
                                                               badge_number=r['result']['badge_num'])
        return player

    def sign_up_player(self, tournament, player, team=False):
        if player.tournament_set.filter(pk=tournament.pk):
            return False, f"You are already signed up for {tournament.name}"
        if not tournament.players.count() < tournament.max_players and not tournament.allow_waitlist:
            return False, f"Sorry {tournament.name} is full"
        if now() < tournament.open_time:
            return False, f"Sorry, {tournament.name} has already started"
        existing_signups = player.tournament_set.filter(start_time=tournament.start_time)
        if existing_signups:
            return False, f"Sorry, you are already signed up for {existing_signups[0].name} at that time"
        tournament.players.add(player)
        if not team:
            signup_player(tournament, player)
        if tournament.players.count() >= tournament.max_players and tournament.allow_waitlist:
            return True, f"Successfully waitlisted for {tournament.name}"
        return True, f"Successfully signed up for {tournament.name}"

    def single_sign_up(self, tournament, barcode):
        player = self.get_create_tournament_player(barcode)
        if player:
            return self.sign_up_player(tournament, player)
        return False, f"Sorry, your badge didn't scan properly, please try again. If the problem persists, please go see registration"

    def team_sign_up(self, tournament, barcodes):
        success = True
        message = []
        players = []
        for barcode in barcodes:
            player = self.get_create_tournament_player(barcode)
            if player:
                players.append(player)
                s, m = self.sign_up_player(tournament, player, team=True)
                if not s:
                    success = False
                    message.append(f"{player.first_name} {player.last_name}: {m}")
                continue
            success = False
            message.append("Sorry, your badge didn't scan properly, please try again. If the problem persists, please go see registration")
        if success:
            t = TournamentTeam.objects.create(tournament=tournament)
            t.players.set(players)
            t.save()
        return success, message

    @staticmethod
    def remove_from_tournament(self, tournament, player):
        # Takes a given tournament and player and removes the player from the tournament
        # Does not throw any errors if the player is not in the tournament
        remove_player(tournament, player)
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
