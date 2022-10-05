from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *


@login_required
def Home(request):
    return render(request, "home.html")

@login_required
def CurrentUserLibrary(request):
    uid = request.user.id
    return UserLibrary(request, uid)

@login_required
def UserLibrary(request, uid):
    movies = Movie.objects.filter(user_libraries__user__id=uid).all()
    movies = movies.order_by('year', 'title')

    shows = Show.objects.filter(user_libraries__user__id=uid).all()
    shows = shows.order_by('title')

    context = {
        'movies' : movies,
        'shows' : shows,
    }

    return render(request, "library.html", context)

@login_required
def MovieDetails(request, id):
    movie = Movie.objects.get(id=id)

    context = {
        'movie' : movie,
    }

    return render(request, "movie.html", context)

@login_required
def ShowDetails(request, id):
    show = Show.objects.get(id=id)

    context = {
        'show' : show,
    }

    return render(request, "show.html", context)