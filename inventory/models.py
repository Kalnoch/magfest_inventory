import django
from django.db import models

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory_system.settings'


# Create your models here.
class Item(models.Model):
    barcode = models.CharField(max_length=64)
    name = models.CharField(max_length=64)  # Human readable name (ie. PS4, Atari 2600, Mario Party 64, 360 controller)
    type = models.CharField(max_length=32)  # Human readable type (ie. Console, Game, Controller, TV, etc)
    checked_out = models.BooleanField(default=False)  # Is the item checked out
    checked_out_by = models.CharField(max_length=128, blank=True)  # Who checked out the item
    location = models.CharField(max_length=64)  # Idea for this one being is it at SUPER, West, Labs, Warehouse?
    serial_number = models.CharField(max_length=128, blank=True)  # Mostly for consoles
    input_type = models.CharField(max_length=128, blank=True)  # Mostly for TVs
    resolution = models.CharField(max_length=128, blank=True)  # Mostly for TVs


class Console(models.Model):
    pass


class Game(models.Model):
    pass


class Peripheral(models.Model):
    pass


class Tournament(models.Model):
    name = models.CharField(max_length=64)  # Name of tournament
    max_players = models.IntegerField()  # Max number of players in the tournament
    start_time = models.DateTimeField()  # When the tournament starts
    open_time = models.DateTimeField()  # When signup opens for the tournament
    m_points = models.IntegerField()  # Number of m-points associated with a tournament
    players = models.ManyToManyField('TournamentPlayer', blank=True)
    printed = models.BooleanField(default=False)  # Whether the tournament bracket has been printed
    # kind_of_bracket

    def __str__(self):
        return self.name


class TournamentPlayer(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    badge_number = models.CharField(max_length=7)

    def __str__(self):
        return " ".join([self.first_name, self.last_name])
