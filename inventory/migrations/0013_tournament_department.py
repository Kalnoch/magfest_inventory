# Generated by Django 4.0.1 on 2022-01-06 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20200101_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='department',
            field=models.CharField(default='Consoles', max_length=64),
        ),
    ]