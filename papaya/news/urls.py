from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='main'),
    path('<int:News_id>/', views.detail, name='news_detail'),
    path('manage_news/', views.manage_news, name='manage_news'),
    path('create_news/', views.create_news, name='create_news'),
    path('edit_news/<int:news_id>/', views.edit_news, name='edit_news'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
]