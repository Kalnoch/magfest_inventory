# Generated by Django 4.1.4 on 2022-12-31 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_tournamentteam_tournament_team_tournament'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='team_tournament',
            new_name='team_size',
        ),
    ]