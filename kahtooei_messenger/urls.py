from django.urls import path
from .views import login,register,checkConnect

urlpatterns = [
    path('connect', checkConnect),
    path('login', login),
    path('register', register),
]
