from django.contrib import admin

from .models import *

# Register your models here.

class MovieMeta(admin.TabularInline):
    model = MovieMeta

class MovieGenreAdmin(admin.TabularInline):
    model = MovieGenre
admin.site.register(Genre)

class MovieDirectorAdmin(admin.TabularInline):
    model = MovieDirectors
admin.site.register(Director)

class MovieWriterAdmin(admin.TabularInline):
    model = MovieWriters
admin.site.register(Writer)

class MovieActorAdmin(admin.TabularInline):
    model = MovieActors
admin.site.register(Actor)

class MovieCompanyAdmin(admin.TabularInline):
    model = MovieCompanies
admin.site.register(Company)

class MovieRatingAdmin(admin.TabularInline):
    model = MovieRating

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'imDbId', 'title', 'year')
    search_fields = ['title', 'imDbId']
    inlines = [MovieMeta, MovieGenreAdmin, MovieDirectorAdmin, MovieWriterAdmin, MovieActorAdmin, MovieCompanyAdmin,MovieRatingAdmin]
    def get_ordering(self, request):
        return ['title']
admin.site.register(Movie, MovieAdmin)


class SeasonAdmin(admin.TabularInline):
    model = Season

class EpisodeAdmin(admin.TabularInline):
    model = Episode

class ShowMetaAdmin(admin.TabularInline):
    model = ShowMeta

class ShowGenreAdmin(admin.TabularInline):
    model = ShowGenre

class ShowDirectorAdmin(admin.TabularInline):
    model = ShowDirectors

class ShowWriterAdmin(admin.TabularInline):
    model = ShowWriters

class ShowActorAdmin(admin.TabularInline):
    model = ShowActors

class ShowCompanyAdmin(admin.TabularInline):
    model = ShowCompanies

class ShowRatingAdmin(admin.TabularInline):
    model = ShowRating

class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'imDbId', 'title', 'year')
    search_fields = ['title', 'imDbId']
    inlines = [SeasonAdmin, EpisodeAdmin, ShowMetaAdmin, ShowGenreAdmin, ShowWriterAdmin, ShowActorAdmin, ShowCompanyAdmin, ShowRatingAdmin]
    def get_ordering(self, request):
        return ['title']
admin.site.register(Show, ShowAdmin)

class EpisodeMetaAdmin(admin.TabularInline):
    model = EpisodeMeta

class EpisodeRatingAdmin(admin.TabularInline):
    model = EpisodeRating

class EpisodeDisplayAdmin(admin.ModelAdmin):
    list_display = ('show', 'season', 'episode_no', 'title')
    search_fields = ['title', 'show']
    inlines = [EpisodeMetaAdmin, EpisodeRatingAdmin]
    def get_ordering(self, request):
        return ['show', 'season', 'episode_no']
admin.site.register(Episode, EpisodeDisplayAdmin)


class UserMovieLibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie')
    def get_ordering(self, request):
        return ['user', 'movie']
admin.site.register(UserMovieLibrary, UserMovieLibraryAdmin)

class UserShowibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show')
    def get_ordering(self, request):
        return ['user', 'show']
admin.site.register(UserShowLibrary, UserShowibraryAdmin)


class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'name')
    def get_ordering(self, request):
        return ['value']
admin.site.register(UserRating, UserRatingAdmin)



