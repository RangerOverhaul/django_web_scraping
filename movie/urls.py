from django.urls import path
from . import views

app_name = "movie"
urlpatterns = [
    path('', views.index, name="index"),
    path('movieList/<str:year>/', views.movieList, name="movieList"),
    path('movieList/<str:year>/edit', views.edit, name="edit"),
    path('moveedit/<str:year>/', views.movieedit, name="moveedit"),
    path('detail/<int:id>/', views.detail, name="detail"),
    path('delete/<int:id>/', views.delete, name="delete"),
]
