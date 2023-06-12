from django.urls import path
from . import views

app_name = 'roulette'
urlpatterns = [
    path('', views.index, name='main'),
    path('add-ticket/<int:ticks>/', views.add_ticket, name='add_ticket'),
    path('remove-ticket/<int:ticks>/', views.remove_ticket, name='remove_ticket'),
    path('buy-tickets/<int:ticks>/', views.buy_tickets, name='buy_tickets'),
    path('prize/<int:game_id>/', views.prize, name='prize'),
]
