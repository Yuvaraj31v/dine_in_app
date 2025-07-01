from django.urls import path
from .views import FoodItemView

urlpatterns = [
    path('foods/', FoodItemView.as_view(), name='food-filter'),
]