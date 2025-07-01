# urls.py

from django.urls import path
from .views import login_view, register_view

# URL patterns for authentication endpoints
urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]
