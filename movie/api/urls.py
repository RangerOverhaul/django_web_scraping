from django.urls import path
from movie.api.api import *

urlpatterns = [
    path('movies/', movie_api, name='movieapi'),
    path('movies/<int:pk>/', movieDetail, name='movieDetail'),
    path('moviespername/<str:name>/', movieForname, name='movieForname'),
    path('moviesperyear/<str:year>/', movieForyear, name='movieForyear'),
]