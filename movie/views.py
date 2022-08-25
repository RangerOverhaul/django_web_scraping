from __future__ import absolute_import, unicode_literals

import time

from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Years
import requests as rq
from .forms import Datay, Datap
from bs4 import BeautifulSoup
from celery import shared_task
from django.http import HttpResponseRedirect
import random

# Create your views here.
# automatic create movie
@shared_task
def add(num):
    time.sleep(1)
    num = int(num)
    tam = int(random.randrange(0, 20))
    yam = int(random.randrange(0, 20))
    num = (tam * 3) - yam * 2
    critics = (num + tam) - (3 * yam)
    to = num - critics
    peli = Movie(title=f'Peli automatica {to}', ids=num, year=f'2020', critics_consensus=critics)
    peli.save()
    return 'New movie was add'

def index(request):
    year = ""
    if request.method == 'POST':
        form = Datay(request.POST)
        if form.is_valid():
            form.save()
            year = form.cleaned_data.get("year")
            add(year)
            return redirect('movieList/'+year)
    else:
        form = Datay()

    tittle = 'Seleccion de peliculas por años.'
    context = {
        'tittle': tittle,
        'form': form,
        'year': year
    }
    return render(request, 'index.html', context)


def movieList(request, year):
    y = year
    if not y.isdigit():
        return redirect('index')
    else:
        num = int(y)
        if num < 1950 or num > 2020:
            return redirect('index')

    url = 'https://www.rottentomatoes.com/top/bestofrt/?year='+y
    page = rq.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    movieses = soup.find_all('a', class_='unstyled articleLink')
    revi = soup.find_all('td', class_='right hidden-xs')
    review = list()
    movies = list()


    for i in movieses:
        if i.text.endswith(")"):
            rem = '('+year+')'
            nombre = i.text.replace(rem, "")
            movies.append(nombre)
            tit = Movie.objects.filter(title=nombre)
            if not tit.exists():
                las = Movie.objects.last()
                id = None
                if las != None:
                    id = las.ids + 1
                else:
                    id = 1
                mov = Movie(ids=id, title=nombre, year=y)
                mov.save()

    count = 0
    for y in revi:
        review.append(y.text)
        try:
            rv = Movie.objects.get(title=movies[count])
        except Exception as e:
            print(str(e))
        else:
            rv.critics_consensus = y.text
            rv.save()
        count += 1

    general = dict(zip(movies, review))
    film = Movie.objects.filter(year=year)
    context = {
        'movies': movies,
        'review': review,
        'general': general,
        'film': film,
        'year': year,
    }
    return render(request, 'moveList.html', context)

def movieedit(request, year):
    y = year
    if not y.isdigit():
        return redirect('index')
    else:
        num = int(y)
        if num < 1950 or num > 2020:
            return redirect('index')

    film = Movie.objects.order_by('ids')
    context = {

        'film': film,
        'year': year,
    }
    return render(request, 'moveList.html', context)


def edit(request, year):
    movies = Movie.objects.filter(year=year)
    add(year)
    context = {
        'movies': movies
    }
    return render(request, 'edit.html', context)


def detail(request, id):
    try:
        film = Movie.objects.get(ids=id)
    except Exception as e:
        message = 'No se encontro la pelicula'
    submitbutton = False
    add(id)
    if request.method == 'POST':
        form = Datap(request.POST)
        if form.is_valid():
            chas = film.ids #id antiguo
            name = film.title
            form.save()
            chan = form.cleaned_data.get('id') #id nuevo
            flis = Movie.objects.filter(id=chan)
            for f in flis:
                if f.title != name:
                    f.ids = chas
                    f.save()
            submitbutton = True
            film.delete()

    else:
        form = Datap()
    context = {
        'film': film,
        'submitbutton': submitbutton,
        'form': form,
    }
    return render(request, 'detail.html', context)

def delete(request, id):
    try:
        flim = Movie.objects.get(ids=id)
    except Exception as e:
        message = 'No se encontro la pelicula'
    year = flim.year
    mov = flim.title
    context = {
        'year': year,
        'mov': mov,
    }
    flim.delete()
    return render(request, 'delete.html', context)
