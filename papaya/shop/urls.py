from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='main'),
    path('<int:games_id>/', views.detail, name='shop_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('manage_shop/', views.manage_shop, name='manage_shop'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('edit_shop/<int:game_id>/', views.edit_shop, name='edit_shop'),
    path('delete_shop/<int:game_id>/', views.delete_shop, name='delete_shop'),
]
