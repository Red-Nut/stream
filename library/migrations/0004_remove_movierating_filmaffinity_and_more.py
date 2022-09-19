# Generated by Django 4.1.1 on 2022-09-18 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_moviemeta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movierating',
            name='filmAffinity',
        ),
        migrations.RemoveField(
            model_name='movierating',
            name='rottenTomatoes',
        ),
        migrations.RemoveField(
            model_name='movierating',
            name='theMovieDb',
        ),
        migrations.AddField(
            model_name='moviemeta',
            name='content_rating',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]
