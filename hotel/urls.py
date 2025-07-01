from django.urls import path

from .views import HotelItemView

urlpatterns = [
    path('hotels/', HotelItemView.as_view(), name='hotel-filter')
]