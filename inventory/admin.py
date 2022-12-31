from django import forms
from django.contrib import admin

from .models import Item, Tournament, TournamentPlayer, TournamentTeam


# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name', 'type', 'checked_out', 'checked_out_by', 'location')


class TournamentAdmin(admin.ModelAdmin):
    department = forms.ChoiceField(choices=(('A', 'Consoles'), ('B', 'Arcade')))
    list_display = ('name', 'department', 'max_players', 'start_time', 'open_time', 'm_points')


class TournamentPlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'badge_number')


admin.site.register(Item, ItemAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentPlayer, TournamentPlayerAdmin)
admin.site.register(TournamentTeam)
