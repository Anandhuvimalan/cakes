from django.urls import path
from . import views

app_name = 'searchapp'

urlpatterns = [
    path('', views.product_search, name='product_search'),
]