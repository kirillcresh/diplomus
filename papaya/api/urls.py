from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('category-list/', views.ProductCategories.as_view(), name="category_list"),
    path('last-news/', views.LastNews.as_view(), name="last_news"),
    path('need-games/', views.GetGame.as_view(), name="need_games"),
    path('game-by-name/', views.GetGameByName.as_view(), name="game_by_name"),
    path('game-by-category/', views.GetGameByCategory.as_view(), name="game_by_category"),
]
