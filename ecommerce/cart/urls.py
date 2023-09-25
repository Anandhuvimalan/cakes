from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('', views.cart_detail, name='cart_detail'),
]
