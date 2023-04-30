from django import forms
from django.forms import ModelForm
from .models import Orders


class OrderForm(ModelForm):

    class Meta:
        model = Orders
        fields = [ 'total']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)