from django import forms
from django.forms import ModelForm
from .models import Games, Comment


class ShopForm(ModelForm):

    class Meta:
        model = Games
        fields = ['title', 'games', 'picture', 'category_class', 'price']

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'rating']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].help_text = 'Здесь пишут отзыв'
        self.fields['text'].label = ''
        self.fields['text'].widget = forms.TextInput(attrs={
            'placeholder': 'Опишите ваши впечатления от покупки',
            'class': 'form-control',
        })

