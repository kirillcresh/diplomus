from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('category-list/', views.ProductCategories.as_view()),
    path('last-news/', views.LastNews.as_view()),
    path('need-games/', views.GetGame.as_view()),
    path('game-by-name/', views.GetGameByName.as_view()),
    path('game-by-category/', views.GetGameByCategory.as_view()),
]
