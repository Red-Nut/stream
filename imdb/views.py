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

    if json_response['results'] is not None:
        for object in json_response['results']:
            result = {
                'id' : object['id'],
                'title' : object['title'],
                'image_url' : object['image'],
                'year' : object['description'],
            }

            movies.append(result)

    else:
        if json_response['errorMessage'] is not None:
            result = {
                'id' : None,
                'title' : json_response['errorMessage'],
                'image_url' : None,
                'year' : "",
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

    if json_response['results'] is not None:
        for object in json_response['results']:
            result = {
                'id' : object['id'],
                'title' : object['title'],
                'image_url' : object['image'],
                'year' : object['description'],
            }

            shows.append(result)
    else:
        if json_response['errorMessage'] is not None:
            result = {
                'id' : None,
                'title' : json_response['errorMessage'],
                'image_url' : None,
                'year' : "",
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
    show_imDbId = imDbId

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
                    ignore = False
                    remove = False
                    if name == "Animation" or name == "Biography" or name == "Family" or name == "History" or name=="Romance" or name=="Sport" or name=="War":
                        ignore = True
                    if name == "Crime" or name == "Fantasy" or name=="Music" or name=="Mystery":
                        remove = True
                    
                    movieGenre = MovieGenre.objects.create(
                        movie = movie,
                        genre = genre,
                        ignore = ignore,
                        remove = remove
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

            # Companies
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
                        print("Error creating company object")
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
                    print("Error creating movie company object")
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

    if json_response['type'] == "TVSeries":
        show = Show.objects.filter(imDbId = imDbId).first()
        if show is None:
            # Show
            try:
                show = Show.objects.create(
                    imDbId = imDbId,
                    title = json_response['title'],
                    year = json_response['year'],
                    image_url = json_response['image'],
                )
    
            except Exception as e:
                print("Error creating show object")
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)

                return redirect("index")

            # Meta Data
            try:
                showMeta = ShowMeta.objects.create(
                    show = show,
                    release_date = json_response['releaseDate'],
                    plot = json_response['plot'],
                    content_rating = json_response['contentRating'],
                )
            except Exception as e:
                print("Error creating show meta object")
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
                    ignore = False
                    remove = False
                    if name == "Animation" or name == "Biography" or name == "Family" or name == "History" or name=="Romance" or name=="Sport" or name=="War":
                        ignore = True
                    if name == "Crime" or name == "Fantasy" or name=="Music" or name=="Mystery":
                        remove = True

                    showGenre = ShowGenre.objects.create(
                        show = show,
                        genre = genre,
                        ignore = ignore,
                        remove = remove
                    )
                except Exception as e:
                    print("Error creating show genre object")
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
                    showDirector = ShowDirectors.objects.create(
                        show = show,
                        director = director
                    )
                except Exception as e:
                    print("Error creating show director object")
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
                    showwriter = ShowWriters.objects.create(
                        show = show,
                        writer = writer
                    )
                except Exception as e:
                    print("Error creating show writer object")
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
                    showActor = ShowActors.objects.create(
                        show = show,
                        actor = actor,
                        character=character
                    )
                except Exception as e:
                    print("Error creating show actor object")
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
                    showActor = ShowActors.objects.filter(show=show, actor=actor).first()
                    if showActor is not None:
                        showActor.star = True   
                        try:
                            showActor.save()
                        except Exception as e:
                            print("Error saving actor as star in show")
                            if hasattr(e, 'message'):
                                print(e.message)
                            else:
                                print(e)
                            return redirect("index")

            # Companies
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
                    showCompany = ShowCompanies.objects.create(
                        show = show,
                        company = company
                    )
                except Exception as e:
                    print("Error creating show company object")
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)
                    return redirect("index")


            # Show Ratings
            try:
                showRating = ShowRating.objects.create(
                    show = show,
                    imDb = json_response['imDbRating'],
                    metacritic = json_response['metacriticRating'],
                )
            except Exception as e:
                print("Error creating show rating object")
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                return redirect("index")
        

        # Add to User Library
        try:
            library = UserShowLibrary.objects.create(
                user = currentUser,
                show = show,
            )
        except Exception as e:
            print("Error adding show to user library")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return redirect("index")

        # Seasons
        for item in json_response['tvSeriesInfo']['seasons']:
            season = Season.objects.create(
                show=show,
                season_id = item,
            )

            # Episodes
            query = 'https://imdb-api.com/api/seasonepisodes/' + settings.IMDB_APIKEY + '/' + show_imDbId + '/' + item
            print(query)
            APIresponse = requests.get(query, headers=headers)

            try:
                season_json_response = json.loads(APIresponse.content.decode("utf-8"))
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)

            for episode_item in season_json_response['episodes']:
                print()
                episode = Episode.objects.create(
                    episode_no = episode_item['episodeNumber'],
                    season = season,
                    show = show,
                    title = episode_item['title'],
                    image_url = episode_item['image']
                )

                episodeMeta = EpisodeMeta.objects.create(
                    episode = episode,
                    plot = episode_item['plot']
                )

                episodRating = EpisodeRating.objects.create(
                    episode = episode,
                    imDb = episode_item['imDbRating']
                )

    
    return redirect("index")
