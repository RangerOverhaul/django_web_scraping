from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie.models import *
from movie.api.serializers import *
from rest_framework import status


@api_view(['GET', 'POST'])
def movie_api(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        # con el many se interpresta que hay mas de una instancia y convierte cada elemento en serializado
        moviSerial = MovieSerializer(movie, many=True)
        return Response(moviSerial.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        movieserial = MovieSerializer(data=request.data)
        if movieserial.is_valid():
            movieserial.save()
            return Response({'message': 'Movie Created successfully'}, status=status.HTTP_201_CREATED)
        return Response(movieserial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movieDetail(request, pk):
    _movie = Movie.objects.filter(ids=pk)

    if _movie.exists():
        _movie = _movie.latest('ids')

        if request.method == 'GET':
            movieserial = MovieSerializer(_movie)
            return Response(movieserial.data, status=status.HTTP_200_OK)

        if request.method == 'PUT':
            movieserial = MovieSerializer(_movie, data=request.data)
            if movieserial.is_valid():
                movieserial.save()
                return Response(movieserial.data, status=status.HTTP_200_OK)
            return Response(movieserial.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DElETE':
            _movie.delete()
            return Response({'message': 'Movie was deleted'}, status=status.HTTP_200_OK)

    return Response({'message': 'Movie does not exists'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST', 'DELETE'])
def movieForname(request, name):
    try:
        _twom = Movie.objects.filter(title__contains=name)
        num = Movie.objects.filter(title__contains=name).count()

    except Exception as e:
        return Response({'message': 'Movie does not exists'}, status=status.HTTP_404_NOT_FOUND)

    if _twom != None:
        if request.method == 'GET':
            if num > 1:
                movieserial = MovieSerializer(_twom, many=True)
                return Response(movieserial.data, status=status.HTTP_200_OK)
            else:
                movieserial = MovieSerializer(_twom)
                return Response(movieserial.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            movieserial = MovieSerializer(data=request.data)
            if movieserial.is_valid():
                movieserial.save()
                return Response({'message': 'Movie Created successfully'}, status=status.HTTP_201_CREATED)
            return Response(movieserial.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DElETE':
            _twom.delete()
            return Response({'message': 'Movie was deleted'}, status=status.HTTP_200_OK)

    return Response({'message': 'Movie does not exists'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def movieForyear(request, year):
    if request.method == 'GET':
        _movies = Movie.objects.filter(year=year)
        if _movies != None:
            moviSerial = MovieSerializer(_movies, many=True)
            return Response(moviSerial.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Movie does not exists'}, status=status.HTTP_404_NOT_FOUND)
