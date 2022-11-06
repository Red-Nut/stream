from django.urls import path

from . import views

urlpatterns = [
    path('search', views.SearchView, name='search'),
    path('search/', views.SearchView, name='search'),

    path('search/<str:searchTerm>/', views.Search),

    path('add/<str:imDbId>/', views.AddToDatabase, name='add_to_database'),
]