from rest_framework import serializers
from shop.models import Category, Games
from news.models import News


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = '__all__'
