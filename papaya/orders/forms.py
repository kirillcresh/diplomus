from django import forms
from django.forms import ModelForm
from .models import Orders, PaymentType, DeliveryPoint


class OrderForm(ModelForm):

    class Meta:
        model = Orders
        fields = ['total', 'delivery_address', 'phone', 'order_date']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


class OrderCreate(ModelForm):
    delivery_address = forms.ModelChoiceField(
        queryset=DeliveryPoint.objects.all()
    )
    payment_type = forms.ModelChoiceField(
        queryset=PaymentType.objects.all()
    )

    class Meta:
        model = Orders
        fields = ['delivery_address', 'phone', 'payment_type']

    def __init__(self, *args, **kwargs):
        super(OrderCreate, self).__init__(*args, **kwargs)
