from django import forms
from django.forms import ModelForm
from .models import Orders


class OrderForm(ModelForm):

    class Meta:
        model = Orders
        fields = ['total', 'delivery_address', 'phone']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


class OrderCreate(ModelForm):

    class Meta:
        model = Orders
        fields = ['delivery_address', 'phone']

    def __init__(self, *args, **kwargs):
        super(OrderCreate, self).__init__(*args, **kwargs)
