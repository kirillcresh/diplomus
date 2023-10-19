from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.http import urlencode
from main.models import Profile
from news.models import News
from orders.models import DeliveryPoint, PaymentType, Orders, OrderProducts
from shop.models import Category, Games, Comment
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .views import *


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


class NewsTests(APITestCase):

    def setUp(self):
        self.author = User.objects.create(
                id=1,
                password=f"password{1}",
                username=f"username{1}",
                email=f"email{1}",
                first_name=f"first_name{1}",
                last_name=f"last_name{1}",
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
        for id in range(1, 5):
            News.objects.create(
                id=id,
                author=self.author,
                title=f"title{id}",
                news=f"news{id}",
                pub_date=f"2022-12-18T0{id}:50:16.939176Z",
                picture=f"picture{id}"
            )

    def test_get_last_news(self):
        getresp = self.client.get(reverse("api:last_news"))
        testresp = News.objects.last()
        serializer = NewsSerializer(testresp, many=False)
        assert(getresp.data, serializer.data)
        self.assertEqual(getresp.status_code, status.HTTP_200_OK)

    def test_get_fail_news(self):
        getresp = self.client.get(reverse("api:last_news"))
        testresp = News.objects.first()
        serializer = NewsSerializer(testresp, many=False)
        self.assertNotEqual(getresp.data, serializer.data)


class GameByNameTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            id=1,
            category=f"category{1}",
            description=f"description{1}"
        )
        for id in range(1, 5):
            Games.objects.create(
                id=id,
                category_class=self.category,
                title=f"title{id}",
                games=f"games{id}",
                picture=f"picture{id}",
                price=id,
                components=f"components{id}",
                min_players=id,
                max_players=id+1,
                recommend_age=id,
                game_time=id,
                vendor=f"vendor{id}",
                discount=id,
                is_active=True
            )

    def test_get_last_news(self):
        getresp = self.client.get(reverse_querystring("api:game_by_name", query_kwargs={'games_search': '1'}))
        testresp = Games.objects.filter(
            Q(title__icontains="1") | Q(games__icontains="1")
        ).first()
        serializer = GameSerializer(testresp, many=False)
        assert(getresp.data, serializer.data)
        self.assertEqual(getresp.status_code, status.HTTP_200_OK)

    def test_get_fail_news(self):
        getresp = self.client.get(reverse_querystring("api:game_by_name", query_kwargs={'games_search': '1'}))
        testresp = Games.objects.filter(
            Q(title__icontains="2") | Q(games__icontains="2")
        ).first()
        serializer = GameSerializer(testresp, many=False)
        self.assertNotEqual(getresp.data, serializer.data)
