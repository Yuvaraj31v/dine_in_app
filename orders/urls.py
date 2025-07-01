from django.urls import path
from .views import CartItemView

urlpatterns = [
    path('cart/', CartItemView.as_view())

]
