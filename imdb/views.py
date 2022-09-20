from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from library.models import *

import requests
import json

@login_required
def SearchView(request):
    return render(request, "search.html")

@login_required
def Search(request, searchTerm):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    # Movies
    query = 'https://imdb-api.com/api/searchMovie/' + settings.IMDB_APIKEY + '/'+ searchTerm
    APIresponse = requests.get(query, headers=headers)

    try:
        json_response = json.loads(APIresponse.content.decode("utf-8"))
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    movies = []

    for object in json_response['results']:
        result = {
            'id' : object['id'],
            'title' : object['title'],
            'image_url' : object['image'],
            'year' : object['description'],
        }

        movies.append(result)

    # TV Shows
    query = 'https://imdb-api.com/api/searchSeries/' + settings.IMDB_APIKEY + '/'+ searchTerm
    APIresponse = requests.get(query, headers=headers)

    try:
        json_response = json.loads(APIresponse.content.decode("utf-8"))
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    shows = []

    for object in json_response['results']:
        result = {
            'id' : object['id'],
            'title' : object['title'],
            'image_url' : object['image'],
            'year' : object['description'],
        }

        shows.append(result)

    context = {
        'searchTerm' : searchTerm,
        'movies' : movies,
        'shows' : shows,
    }

    return render(request, "search.html", context)

@login_required
def AddToDatabase(request, imDbId):
    currentUser = request.user


    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    query = 'https://imdb-api.com/en/api/title/' + settings.IMDB_APIKEY + '/'+ imDbId
    APIresponse = requests.get(query, headers=headers)

    try:
        json_response = json.loads(APIresponse.content.decode("utf-8"))
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    if json_response['type'] == "Movie":
        movie=Movie.objects.filter(imDbId = imDbId).first()
        if movie is None:
            # Movie
            try:
                movie = Movie.objects.create(
                    imDbId = imDbId,
                    title = json_response['title'],
                    year = json_response['year'],
                    image_url = json_response['image'],
                )
    
            except Exception as e:
                print("Error creating movie object")
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)

                return redirect("index")

            # Meta Data
            try:
                movieMeta = MovieMeta.objects.create(
                    movie = movie,
                    release_date = json_response['releaseDate'],
                    runtime_mins = json_response['runtimeMins'],
                    runtime_str = json_response['runtimeStr'],
                    plot = json_response['plot'],
                    content_rating = json_response['contentRating'],
                )
            except Exception as e:
                print("Error creating movie meta object")
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                return redirect("index")

            # Genres
            for item in json_response['genreList']:
                name=item['value']
                genre = Genre.objects.filter(name=name).first()
                if genre is None:
                    try:
                        genre = Genre.objects.create(
                            name=name
                        )
                    except Exception as e:
                        print("Error creating genre object")
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                        return redirect("index")                    
                try:
                    movieGenre = MovieGenre.objects.create(
                        movie = movie,
                        genre = genre
                    )
                except Exception as e:
                    print("Error creating movie genre object")
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)
                    return redirect("index")

            # Directors
            for item in json_response['directorList']:
                imDbId=item['id']
                name=item['name']
                director = Director.objects.filter(imDbId=imDbId).first()
                if director is None:
                    try:
                        director = Director.objects.create(
                            imDbId=imDbId,
                            name=name
                        )
                    except Exception as e:
                        print("Error creating director object")
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                        return redirect("index")                    
                try:
                    movieDirector = MovieDirectors.objects.create(
                        movie = movie,
                        director = director
                    )
                except Exception as e:
                    print("Error creating movie director object")
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)
                    return redirect("index")

            # Writers
            for item in json_response['writerList']:
                imDbId=item['id']
                name=item['name']
                writer = Writer.objects.filter(imDbId=imDbId).first()
                if writer is None:
                    try:
                        writer = Writer.objects.create(
                            imDbId=imDbId,
                            name=name
                        )
                    except Exception as e:
                        print("Error creating writer object")
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                        return redirect("index")                    
                try:
                    moviewriter = MovieWriters.objects.create(
                        movie = movie,
                        writer = writer
                    )
                except Exception as e:
                    print("Error creating movie writer object")
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)
                    return redirect("index")

            # Actors
            for item in json_response['actorList']:
                imDbId=item['id']
                name=item['name']
                image_url = item['image']
                character = item['asCharacter']
                actor = Actor.objects.filter(imDbId=imDbId).first()
                if actor is None:
                    try:
                        actor = Actor.objects.create(
                            imDbId=imDbId,
                            name=name,
                            image_url=image_url
                        )
                    except Exception as e:
                        print("Error creating actor object")
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                        return redirect("index")                    
                try:
                    movieActor = MovieActors.objects.create(
                        movie = movie,
                        actor = actor,
                        character=character
                    )
                except Exception as e:
                    print("Error creating movie actor object")
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)
                    return redirect("index")

            # Stars
            for item in json_response['starList']:
                imDbId=item['id']
                actor = Actor.objects.filter(imDbId=imDbId).first()
                if actor is not None:
                    movieActor = MovieActors.objects.filter(movie=movie, actor=actor).first()
                    if movieActor is not None:
                        movieActor.star = True   
                        try:
                            movieActor.save()
                        except Exception as e:
                            print("Error saving actor as star in movie")
                            if hasattr(e, 'message'):
                                print(e.message)
                            else:
                                print(e)
                            return redirect("index")

            # Actors
            for item in json_response['companyList']:
                imDbId=item['id']
                name=item['name']
                company = Company.objects.filter(imDbId=imDbId).first()
                if company is None:
                    try:
                        company = Company.objects.create(
                            imDbId=imDbId,
                            name=name
                        )
                    except Exception as e:
                        print("Error creating actor object")
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                        return redirect("index")                    
                try:
                    movieCompany = MovieCompanies.objects.create(
                        movie = movie,
                        company = company
                    )
                except Exception as e:
                    print("Error creating movie actor object")
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)
                    return redirect("index")


            # Movie Ratings
            try:
                movieRating = MovieRating.objects.create(
                    movie = movie,
                    imDb = json_response['imDbRating'],
                    metacritic = json_response['metacriticRating'],
                )
            except Exception as e:
                print("Error creating movie rating object")
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                return redirect("index")
        

        # Add to User Library
        try:
            library = UserMovieLibrary.objects.create(
                user = currentUser,
                movie = movie,
            )
        except Exception as e:
            print("Error adding movie to user library")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return redirect("index")


        
    
    return redirect("index")
