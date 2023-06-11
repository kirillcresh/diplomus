from django.contrib import admin
from .models import Orders, OrderProducts, DeliveryPoint, PaymentType

admin.site.register(Orders)
admin.site.register(OrderProducts)
admin.site.register(DeliveryPoint)
admin.site.register(PaymentType)
