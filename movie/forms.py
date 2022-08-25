from django import forms
from django.forms import inlineformset_factory, ModelForm
from movie.models import Movie, Years
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Datay(forms.ModelForm):
    class Meta:
        model = Years
        fields = ['year']


class Datap(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'