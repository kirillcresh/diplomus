from django.shortcuts import render, redirect
from .models import News
from datetime import *
from .forms import NewsForm


def index(request):
    news = News.objects.all().order_by('-pub_date')
    context = {
        'news': news,
    }
    return render(request, 'news/index.html', context)


def detail(request, News_id):
    new = News.objects.get(pk=News_id)
    context = {
        'new': new,
    }
    return render(request, 'news/news_detail.html', context)


def manage_news(request):
    if request.user.is_staff:
        news = News.objects.all()
        context = {
            'news': news,
        }
        return render(request, 'news/manage_news.html', context)
    else:
        return redirect('main:main')


def create_news(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                news_form = form.save(commit=False)
                news_form.pub_date = datetime.now()
                news_form.save()
                return redirect('news:manage_news')
        else:
            form = NewsForm()
        return render(request, 'news/create_news.html', {'form': form})
    else:
        return redirect('main:main')


def edit_news(request, news_id):
    if request.user.is_staff:
        news_item = News.objects.get(pk=news_id)
        if request.method == "POST":
            form = NewsForm(request.POST, request.FILES, instance=news_item)
            if form.is_valid():
                news_form = form.save(commit=False)
                news_form.pub_date = datetime.now()
                news_form.save()
                return redirect('news:manage_news')
        else:
            form = NewsForm(instance=news_item)
        return render(request, 'news/edit_news.html', {'form': form})
    else:
        return redirect('main:main')


def delete_news(request, news_id):
    if request.user.is_staff:
        news_item = News.objects.get(pk=news_id)
        news_item.delete()
        return redirect('news:manage_news')
    else:
        return redirect('main:main')