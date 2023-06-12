import random

from django.shortcuts import render, redirect
from shop.models import Games
from orders.models import Orders, OrderProducts
from main.models import Profile

from django.conf import settings


def index(request):
    tickets = str(request.GET.get("tickets"))
    profile = Profile.objects.get(client_id=request.user)
    context = {"profile": profile}
    if tickets.isnumeric():
        ticks = int(tickets)
        context["ticks"] = ticks
    if request.method == "POST" and profile.tickets > 0:
        items = list(Games.objects.all())
        item = random.choice(items)
        context["item"] = item
        profile.tickets -= 1
        profile.save()
        return render(request, "roulette/index.html", context)
    return render(request, "roulette/index.html", context)


def add_ticket(request, ticks):
    ticks += 1
    return redirect(f"{settings.BASE_URL}/roulette/?tickets={ticks}")


def remove_ticket(request, ticks):
    if ticks < 2:
        pass
    else:
        ticks -= 1
    return redirect(f"{settings.BASE_URL}/roulette/?tickets={ticks}")


def buy_tickets(request, ticks):
    profile = Profile.objects.get(client_id=request.user)
    profile.tickets += ticks
    profile.save()
    return redirect(f"{settings.BASE_URL}/roulette/?tickets=1")


def prize(request, game_id):
    if request.user.is_active:
        game = Games.objects.get(id=game_id)
        try:
            cart = Orders.objects.get(client=request.user, is_cart=True)
        except:
            cart = Orders.objects.create(client=request.user)
        try:
            check = OrderProducts.objects.get(games_id=game, order_id=cart)
            if check.discount == 100:
                check.amount += 1
                check.save()
            else:
                check.amount = 1
                check.discount = 100
                check.save()
        except:
            prod = OrderProducts()
            prod.games_id = game
            prod.order_id = cart
            prod.amount = 1
            prod.discount = 100
            prod.save()
        return redirect("orders:cart_detail")
    else:
        return redirect("main:main")
