# Generated by Django 2.1.3 on 2018-11-03 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20181103_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(default='blank', max_length=32),
            preserve_default=False,
        ),
    ]
