from django.urls import path

from carts.views import *
app_name = 'carts'

urlpatterns = [
    path('cart/add/', CartAddView.as_view(), name='cart_add'),
    path('cart/change/', CartChangeView.as_view(), name='cart_change'),
    path('cart/remove/', CartRemoveView.as_view(), name='cart_remove'),
]

