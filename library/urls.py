from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home, name='index'),

    path('library',views.CurrentUserLibrary, name='library'),
    path('library/<int:uid>',views.UserLibrary, name='user_library'),

    path('movie/<int:id>',views.MovieDetails, name='movie'),
    path('series/<int:id>',views.ShowDetails, name='show'),
]