# Generated by Django 4.1.4 on 2022-12-31 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_alter_tournament_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='info_only_tournament',
            field=models.BooleanField(default=False),
        ),
    ]
