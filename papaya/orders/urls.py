from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.index, name='main'),
    path('<int:Orders_id>/', views.detail, name='orders_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add_item/<int:id>', views.add_item, name='add_item'),
    path('remove_item/<int:id>', views.remove_item, name='remove_item'),
    path('order_create/', views.order_create, name='order_create'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
    path('manage_order/', views.manage_order, name='manage_order'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
