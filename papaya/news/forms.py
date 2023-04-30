from django import forms
from django.forms import ModelForm
from .models import News


class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = ['title', 'news', 'picture', 'author']

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)


