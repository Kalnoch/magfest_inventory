# Generated by Django 4.0.1 on 2022-01-06 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_tournament_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='department',
            field=models.CharField(choices=[('Consoles', 'Consoles'), ('Arcade', 'Arcade')], max_length=64),
        ),
    ]