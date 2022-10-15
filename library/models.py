from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

class Director(models.Model):
    name = models.CharField(max_length=255)
    imDbId = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

class Writer(models.Model):
    name = models.CharField(max_length=255)
    imDbId = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

class Actor(models.Model):
    name = models.CharField(max_length=255)
    imDbId = models.CharField(max_length=20, unique=True)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=255)
    imDbId = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"



class Movie(models.Model):
    imDbId = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    @property
    def genres_prop(self):
        genres = ""
        for genre in self.genres.all():
            if not genre.ignore and not genre.remove:
                genres += genre.genre.name + ", "

        if genres != "":
            genres = genres[:-2]
        return genres

    @property
    def ignored_genres_prop(self):
        genres = ""
        for genre in self.genres.all():
            if genre.ignore and not genre.remove:
                genres += genre.genre.name + ", "

        if genres != "":
            genres = genres[:-2]
        return genres

    @property
    def removed_genres_prop(self):
        genres = ""
        for genre in self.genres.all():
            if genre.remove:
                genres += genre.genre.name + ", "

        if genres != "":
            genres = genres[:-2]
        return genres

class MovieMeta(models.Model):
    movie = models.OneToOneField(Movie,on_delete=models.CASCADE, related_name="mete_data")
    release_date = models.DateField()
    runtime_mins = models.IntegerField()
    runtime_str = models.CharField(max_length=10)
    plot = models.CharField(max_length=1000)
    content_rating = models.CharField(max_length=25)

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="genres")
    genre = models.ForeignKey(Genre,on_delete=models.RESTRICT, related_name="movies")
    ignore = models.BooleanField(default=False)
    remove = models.BooleanField(default=False)

class MovieGenreProxy(Movie):
    class Meta:
        proxy = True


class MovieDirectors(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="directors")
    director = models.ForeignKey(Director,on_delete=models.RESTRICT, related_name="movies")

class MovieWriters(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="writers")
    writer = models.ForeignKey(Writer,on_delete=models.RESTRICT, related_name="movies")

class MovieActors(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="actors")
    actor = models.ForeignKey(Actor,on_delete=models.RESTRICT, related_name="movies")
    character = models.CharField(max_length=100)
    star = models.BooleanField(default=False)

class MovieCompanies(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="companies")
    company = models.ForeignKey(Company,on_delete=models.RESTRICT, related_name="movies")

class MovieRating(models.Model):
    movie = models.OneToOneField(Movie,on_delete=models.CASCADE, related_name="ratings")
    imDb = models.DecimalField(max_digits=5, decimal_places=1)
    metacritic = models.DecimalField(max_digits=5, decimal_places=1)
    #theMovieDb = models.DecimalField(max_digits=5, decimal_places=1)
    #rottenTomatoes = models.IntegerField()
    #filmAffinity = models.DecimalField(max_digits=5, decimal_places=1)

class Show(models.Model):
    imDbId = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}"

    @property
    def genres_prop(self):
        genres = ""
        for genre in self.genres.all():
            if not genre.ignore and not genre.remove:
                genres += genre.genre.name + ", "

        if genres != "":
            genres = genres[:-2]
        return genres

    @property
    def ignored_genres_prop(self):
        genres = ""
        for genre in self.genres.all():
            if genre.ignore and not genre.remove:
                genres += genre.genre.name + ", "

        if genres != "":
            genres = genres[:-2]
        return genres

    @property
    def removed_genres_prop(self):
        genres = ""
        for genre in self.genres.all():
            if genre.remove:
                genres += genre.genre.name + ", "

        if genres != "":
            genres = genres[:-2]
        return genres

class ShowMeta(models.Model):
    show = models.OneToOneField(Show,on_delete=models.CASCADE, related_name="mete_data")
    release_date = models.DateField()
    plot = models.CharField(max_length=1000)
    content_rating = models.CharField(max_length=25)

class Season(models.Model):
    show = models.ForeignKey(Show, related_name="seasons", on_delete=models.CASCADE)
    season_id = models.CharField(max_length=10)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"Season {self.season_id}"

class Episode(models.Model):
    episode_no = models.CharField(max_length=10)
    season = models.ForeignKey(Season,null=True, blank=True, related_name="episodes", on_delete=models.CASCADE)
    show = models.ForeignKey(Show,null=True, blank=True, related_name="episodes", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"Episode {self.episode_no}"

class EpisodeMeta(models.Model):
    episode = models.OneToOneField(Episode,on_delete=models.CASCADE, related_name="mete_data")
    plot = models.CharField(max_length=1000)

class EpisodeRating(models.Model):
    episode = models.OneToOneField(Episode,on_delete=models.CASCADE, related_name="ratings")
    imDb = models.DecimalField(max_digits=5, decimal_places=1)


    
class ShowGenre(models.Model):
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name="genres")
    genre = models.ForeignKey(Genre,on_delete=models.RESTRICT, related_name="shows")
    ignore = models.BooleanField(default=False)
    remove = models.BooleanField(default=False)

class ShowGenreProxy(Show):
    class Meta:
        proxy = True

class ShowDirectors(models.Model):
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name="directors")
    director = models.ForeignKey(Director,on_delete=models.RESTRICT, related_name="shows")

class ShowWriters(models.Model):
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name="writers")
    writer = models.ForeignKey(Writer,on_delete=models.RESTRICT, related_name="shows")

class ShowActors(models.Model):
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name="actors")
    actor = models.ForeignKey(Actor,on_delete=models.RESTRICT, related_name="shows")
    character = models.CharField(max_length=100)
    star = models.BooleanField(default=False)

class ShowCompanies(models.Model):
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name="companies")
    company = models.ForeignKey(Company,on_delete=models.RESTRICT, related_name="shows")

class ShowRating(models.Model):
    show = models.OneToOneField(Show,on_delete=models.CASCADE, related_name="ratings")
    imDb = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    metacritic = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    #theMovieDb = models.DecimalField(max_digits=5, decimal_places=1)
    #rottenTomatoes = models.IntegerField()
    #filmAffinity = models.DecimalField(max_digits=5, decimal_places=1)







class UserRating(models.Model):
    value = models.IntegerField()
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"

class UserMovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.ForeignKey(UserRating, on_delete=models.RESTRICT)

class UserShowRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    rating = models.ForeignKey(UserRating, on_delete=models.RESTRICT)

class UserSeasonRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    rating = models.ForeignKey(UserRating, on_delete=models.RESTRICT)





class UserMovieLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_movies")
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="user_libraries")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user','movie'], name='unique_movie'),
        ]

class UserShowLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_shows")
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name="user_libraries")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user','show'], name='unique_show'),
        ]



