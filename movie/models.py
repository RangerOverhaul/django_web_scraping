from django.db import models


# Create your models here.
class Movie(models.Model):
    ids = models.IntegerField('ID')
    title = models.CharField('Titulo', max_length=255, unique=True, blank=True)
    critics_consensus = models.CharField('Numero de críticas', max_length=255, blank=True, null=True)
    year = models.CharField('Año de lanzamiento', max_length=4, unique=False, blank=True)

    def __str__(self):
        return self.title


class Years(models.Model):
    year = models.CharField(max_length=4, unique=False, blank=True)

    def __str__(self):
        return self.year
