from django.shortcuts import render
from rest_framework import viewsets

from reviews.models import Category, Genre,  Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer  


