# Generated by Django 4.1.1 on 2022-09-18 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_remove_movierating_filmaffinity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('imDbId', models.CharField(max_length=20)),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('imDbId', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('imDbId', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('imDbId', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='moviemeta',
            name='movie',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mete_data', to='library.movie'),
        ),
        migrations.AlterField(
            model_name='movierating',
            name='movie',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='library.movie'),
        ),
        migrations.CreateModel(
            name='MovieWriters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='writers', to='library.movie')),
                ('writer', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='movies', to='library.writer')),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='movies', to='library.genre')),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='library.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieDirectors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='movies', to='library.director')),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='directors', to='library.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='movies', to='library.company')),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='library.movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieActors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False)),
                ('actor', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='movies', to='library.actor')),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='library.movie')),
            ],
        ),
    ]
