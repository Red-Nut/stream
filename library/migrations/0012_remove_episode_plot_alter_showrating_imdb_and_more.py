# Generated by Django 4.1.1 on 2022-09-20 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_remove_episode_eipsode_no_episode_episode_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='plot',
        ),
        migrations.AlterField(
            model_name='showrating',
            name='imDb',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='showrating',
            name='metacritic',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
    ]