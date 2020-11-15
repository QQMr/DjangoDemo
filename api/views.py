from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from .models import Movie, Rating
from .serializers import UserSerializer,MovieSerializer, RatingSerializer
from django.contrib.auth.models import User

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]

    @action(detail=True, methods=['Post'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print('user', user)
            #user = User.objects.get(id=2)
            print('user', user.username)

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
            except:
                Rating.objects.create(user=user, movie=movie, stars=stars)

            reponse = {'message': 'its working'}
            return Response(reponse, status=status.HTTP_200_OK)
        else:
            reponse = {'message': 'not working, please enter stars'}
            return Response(reponse, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [ TokenAuthentication ]
