from __future__ import absolute_import, unicode_literals
from celery import shared_task
from movie.models import Movie
import time

@shared_task
def add(num):
    time.sleep(20)
    num = (num * 2) + 3
    critics = (num + 20) * 3
    peli = Movie(title='Peli automatica 1', ids=num, year='2020', critics_consensus=critics)
    peli.save()
    return 'New movie was add'
