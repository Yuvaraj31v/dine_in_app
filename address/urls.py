from django.urls import path
from .views import AddressItemView

urlpatterns = [
    path('address/', AddressItemView.as_view(), name='address-filter'),
]