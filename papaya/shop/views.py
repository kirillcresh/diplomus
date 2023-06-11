from datetime import *

from django.shortcuts import redirect, render, get_object_or_404

from orders.models import OrderProducts, Orders

from .forms import CommentForm, ShopForm
from .models import Category, Comment, Games


def index(request):
    categories = Category.objects.all().order_by("-category")
    sort = str(request.GET.get("name"))
    filtrate_by = str(request.GET.get("filtrate_by"))
    boolka = 0
    if sort != "None":
        title = Category.objects.get(id=int(sort)).category
        if filtrate_by == "price_up":
            games = Games.objects.filter(
                category_class=int(sort), is_active=True
            ).order_by("price")
        elif filtrate_by == "price_down":
            games = Games.objects.filter(
                category_class=int(sort), is_active=True
            ).order_by("-price")
        else:
            games = Games.objects.filter(
                category_class=int(sort), is_active=True
            ).order_by("title")
        boolka = 1
        
    else:
        if filtrate_by == "price_up":
            games = Games.objects.all().order_by("price")
        elif filtrate_by == "price_down":
            games = Games.objects.all().order_by("-price")
        else:
            games = Games.objects.all().order_by("title")
        title = "Все товары"
    context = {
        "flag": sort,
        "boolka": boolka,
        "games": games,
        "categories": categories,
        "title": title,
    }
    return render(request, "shop/index.html", context)


def detail(request, games_id):
    game = Games.objects.get(pk=games_id)
    comments = Comment.objects.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            com_fom = form.save(commit=False)
            com_fom.author = request.user
            com_fom.game = game
            com_fom.pub_date = datetime.now()
            com_fom.save()
            form = CommentForm()
            context = {
                "game": game,
                "form": form,
                "comments": comments,
            }
            return render(request, "shop/shop_detail.html", context)
    form = CommentForm()

    context = {
        "game": game,
        "form": form,
        "comments": comments,
    }
    return render(request, "shop/shop_detail.html", context)


def add_to_cart(request, product_id):
    if request.user.is_active:
        game = Games.objects.get(id=product_id)

        try:
            cart = Orders.objects.get(client=request.user, is_cart=True)
        except:
            cart = Orders.objects.create(client=request.user)

        try:
            check = OrderProducts.objects.get(games_id=game, order_id=cart)
            if check.discount == 100:
                return redirect("orders:cart_detail")
            check.amount += 1
            check.discount = game.discount
            check.save()
            cart.total += check.get_discount_price()
            cart.save()
        except:
            prod = OrderProducts()
            prod.games_id = game
            prod.order_id = cart
            prod.amount = 1
            prod.discount = game.discount
            prod.save()
            cart.total += prod.get_discount_price()
            cart.save()
        return redirect("orders:cart_detail")
    else:
        return redirect("main:main")


def manage_shop(request):
    if request.user.is_staff:
        games = Games.objects.all()
        context = {
            "games": games,
        }
        return render(request, "shop/manage_shop.html", context)
    else:
        return redirect("main:main")


def create_shop(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = ShopForm(request.POST, request.FILES)
            if form.is_valid():
                game_form = form.save(commit=False)
                game_form.save()
                return redirect("shop:manage_shop")
        else:
            form = ShopForm()
        return render(request, "shop/create_shop.html", {"form": form})
    else:
        return redirect("main:main")


def edit_shop(request, game_id):
    if request.user.is_staff:
        game_item = Games.objects.get(pk=game_id)
        if request.method == "POST":
            form = ShopForm(request.POST, request.FILES, instance=game_item)
            if form.is_valid():
                game_form = form.save(commit=False)
                game_form.save()
                return redirect("shop:manage_shop")
        else:
            form = ShopForm(instance=game_item)
        return render(request, "shop/edit_shop.html", {"form": form})
    else:
        return redirect("main:main")


def delete_shop(request, game_id):
    if request.user.is_staff:
        game_item = Games.objects.get(pk=game_id)
        game_item.delete()
        return redirect("shop:manage_shop")
    else:
        return redirect("main:main")
