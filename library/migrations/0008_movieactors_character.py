# Generated by Django 4.1.1 on 2022-09-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_movieactors_actor_alter_movieactors_movie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieactors',
            name='character',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
