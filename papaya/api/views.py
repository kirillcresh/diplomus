from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Category, Games
from news.models import News

from .serializers import CategorySerializer, NewsSerializer, GameSerializer


class ProductCategories(APIView):
    def get(self, request):
        data = Category.objects.all()
        serializer = CategorySerializer(data, many=True)
        return Response(serializer.data)


class LastNews(APIView):
    def get(self, request):
        data = News.objects.last()
        serializer = NewsSerializer(data, many=False)
        return Response(serializer.data)


class GetGame(APIView):
    def get(self, request):
        data = Games.objects.all()
        serializer = GameSerializer(data, many=True)
        return Response(serializer.data)


class GetGameByName(APIView):
    def get(self, request):
        games_search = self.request.query_params.get("games_search")
        data = Games.objects.filter(
            Q(title__icontains=games_search) | Q(games__icontains=games_search)
        ).first()
        serializer = GameSerializer(data, many=False)
        print(serializer.data)
        if not data:
            raise Exception
        return Response(serializer.data)


class GetGameByCategory(APIView):
    def get(self, request):
        cat_games_search = self.request.query_params.get("cat_games_search")
        id_cat = Category.objects.get(category__icontains=cat_games_search).id
        data = Games.objects.filter(category_class=id_cat)
        serializer = GameSerializer(data, many=True)
        print(serializer.data)
        if not data:
            raise Exception
        return Response(serializer.data)
