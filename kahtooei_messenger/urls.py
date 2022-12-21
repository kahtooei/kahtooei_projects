from django.urls import path
from .views import login,register,checkConnect,newChat

urlpatterns = [
    path('connect', checkConnect),
    path('login', login),
    path('register', register),
    path('newChat', newChat),
]
