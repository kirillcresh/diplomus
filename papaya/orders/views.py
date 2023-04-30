from django.shortcuts import render, redirect
from .models import Orders, OrderProducts
from shop.models import Games
from orders.forms import OrderForm


def index(request):
    if request.user.is_active:
        orders = Orders.objects.filter(is_cart=False).order_by('-total')
        context = {
            'orders': orders,
        }
        return render(request, 'orders/index.html', context)
    else:
        return redirect('main:main')


def detail(request, Orders_id):
    if request.user.is_active:
        ord = Orders.objects.get(pk=Orders_id)
        order_products = OrderProducts.objects.filter(order_id=ord)
        games = Games.objects.all()
        context = {
            'ord': ord,
            'order_products': order_products,
            'games': games,
        }
        return render(request, 'orders/orders_detail.html', context)
    else:
        return redirect('main:main')


def cart_detail(request):
    if request.user.is_active:
        try:
            cart = Orders.objects.get(client=request.user, is_cart=True)
        except:
            cart = Orders.objects.create(client=request.user)
        order_prods = OrderProducts.objects.filter(order_id=cart.id)
        games = Games.objects.all()
        context = {
            'cart': cart,
            'order_prods': order_prods,
            'games': games,
        }
        return render(request, 'orders/cart_detail.html', context)
    else:
        return redirect('main:main')


def add_item(request, id):
    if request.user.is_active:
        game = OrderProducts.objects.get(id=id)
        game.amount += 1
        game.save()
        cart = Orders.objects.get(client=request.user, is_cart=True)
        cart.total += Games.objects.get(title=game.games_id).price
        cart.save()
        return redirect('orders:cart_detail')
    else:
        return redirect('main:main')


def remove_item(request, id):
    if request.user.is_active:
        game = OrderProducts.objects.get(id=id)
        game.amount -= 1
        game.save()
        cart = Orders.objects.get(client=request.user, is_cart=True)
        cart.total -= Games.objects.get(title=game.games_id).price
        cart.save()
        if game.amount < 1:
            game.delete()
        return redirect('orders:cart_detail')
    else:
        return redirect('main:main')


def order_create(request):
    if request.user.is_active:
        order = Orders.objects.get(client=request.user, is_cart=True)
        order.is_cart = False
        order.save()
        return redirect('orders:main')
    else:
        return redirect('main:main')


def cart_delete(request):
    if request.user.is_active:
        cart = Orders.objects.get(client=request.user, is_cart=True)
        prods = OrderProducts.objects.filter(order_id=cart)
        for prod in prods:
            prod.delete()
        return redirect('orders:cart_detail')
    else:
        return redirect('main:main')


def manage_order(request):
    if request.user.is_staff:
        orders = Orders.objects.all()
        context = {
            'orders': orders,
        }
        return render(request, 'orders/manage_order.html', context)
    else:
        return redirect('main:main')


def edit_order(request, order_id):
    if request.user.is_staff:
        order_item = Orders.objects.get(pk=order_id)
        if request.method == "POST":
            form = OrderForm(request.POST, request.FILES, instance=order_item)
            if form.is_valid():
                game_form = form.save(commit=False)
                game_form.save()
                return redirect('orders:manage_order')
        else:
            form = OrderForm(instance=order_item)
        return render(request, 'orders/edit_order.html', {'form': form})
    else:
        return redirect('main:main')


def delete_order(request, order_id):
    if request.user.is_staff:
        order_item = Games.objects.get(pk=order_id)
        order_item.delete()
        return redirect('orders:manage_order')
    else:
        return redirect('main:main')