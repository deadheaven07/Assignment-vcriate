from django.urls import path
from .views import calculate_price

urlpatterns = [
    path('calculate/', calculate_price, name='calculate_price'),
]
