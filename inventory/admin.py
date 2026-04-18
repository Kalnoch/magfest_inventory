from django import forms
from django.contrib import admin

from .baserow import list_rows
from .challonge import create_tournament, update_tournament
from .models import Item, Tournament, TournamentPlayer, TournamentTeam, Game


# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name', 'type', 'checked_out', 'checked_out_by', 'location')


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'max_players', 'start_time', 'open_time', 'm_points')
    list_filter = ['department']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            tournament = create_tournament(obj)
            obj.challonge_id = tournament['id']
            obj.challonge_url = f"https://challonge.com/{tournament['url']}"
            obj.save()
        else:
            update_tournament(obj)


class TournamentPlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'badge_number')


def sync_baserow(modeladmin, request, queryset):
    modeladmin.model.objects.all().delete()
    fields = modeladmin.get_fields(request)
    baserow_rows = list_rows(modeladmin.baserow_table_id)
    for item in baserow_rows.values():
        field_dict = {field: item[field] for field in fields}
        modeladmin.model.objects.create(**field_dict)


class GameAdmin(admin.ModelAdmin):
    baserow_table_id = 1369
    list_display = ('name', 'console')
    actions = [sync_baserow]


admin.site.register(Item, ItemAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentPlayer, TournamentPlayerAdmin)
admin.site.register(TournamentTeam)
admin.site.register(Game, GameAdmin)
