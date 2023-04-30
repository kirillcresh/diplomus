from datetime import *
from django.shortcuts import render, redirect
from .models import Games, Category, Comment
from orders.models import OrderProducts, Orders
from .forms import ShopForm, CommentForm


def index(request):
    categories = Category.objects.all().order_by('-category')
    sortir = str(request.GET.get('name'))
    if sortir != 'None':
        title = Category.objects.get(id=int(sortir)).category
        games = Games.objects.filter(category_class=int(sortir), is_active=True).order_by('price')
    else:
        games = Games.objects.all().order_by('price')
        title = 'Все товары'
    context = {
        'games': games,
        'categories': categories,
        'title': title,
    }
    return render(request, 'shop/index.html', context)


def detail(request, Games_id):
    game = Games.objects.get(pk=Games_id)
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
                'game': game,
                'form': form,
                'comments': comments,
            }
            return render(request, 'shop/shop_detail.html', context)
    form = CommentForm()

    context = {
        'game': game,
        'form': form,
        'comments': comments,
    }
    return render(request, 'shop/shop_detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_active:
        game = Games.objects.get(id=product_id)

        try:
            cart = Orders.objects.get(client=request.user, is_cart=True)
        except:
            cart = Orders.objects.create(client=request.user)


        try:
            check = OrderProducts.objects.get(games_id=game, order_id=cart)
            print(check)
            check.amount += 1
            check.save()
            cart.total += game.price
            cart.save()
        except:
            prod = OrderProducts()
            prod.games_id = game
            prod.order_id = cart
            prod.amount = 1
            prod.save()
            cart.total += game.price
            cart.save()
        return redirect('orders:cart_detail')
    else:
        return redirect('main:main')


def manage_shop(request):
    if request.user.is_staff:
        games = Games.objects.all()
        context = {
            'games': games,
        }
        return render(request, 'shop/manage_shop.html', context)
    else:
        return redirect('main:main')


def create_shop(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = ShopForm(request.POST, request.FILES)
            if form.is_valid():
                game_form = form.save(commit=False)
                game_form.save()
                return redirect('shop:manage_shop')
        else:
            form = ShopForm()
        return render(request, 'shop/create_shop.html', {'form': form})
    else:
        return redirect('main:main')


def edit_shop(request, game_id):
    if request.user.is_staff:
        game_item = Games.objects.get(pk=game_id)
        if request.method == "POST":
            form = ShopForm(request.POST, request.FILES, instance=game_item)
            if form.is_valid():
                game_form = form.save(commit=False)
                game_form.save()
                return redirect('shop:manage_shop')
        else:
            form = ShopForm(instance=game_item)
        return render(request, 'shop/edit_shop.html', {'form': form})
    else:
        return redirect('main:main')


def delete_shop(request, game_id):
    if request.user.is_staff:
        game_item = Games.objects.get(pk=game_id)
        game_item.delete()
        return redirect('shop:manage_shop')
    else:
        return redirect('main:main')