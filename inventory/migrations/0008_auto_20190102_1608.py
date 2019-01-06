# Generated by Django 2.1.4 on 2019-01-02 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20181130_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentplayer',
            name='tournaments',
        ),
        migrations.AddField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(blank=True, to='inventory.TournamentPlayer'),
        ),
    ]
