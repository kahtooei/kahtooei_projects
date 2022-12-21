from django.urls import path
from .views import login,register,checkConnect,newChat,createGroup

urlpatterns = [
    path('connect', checkConnect),
    path('login', login),
    path('register', register),
    path('newChat', newChat),
    path('createGroup', createGroup),
]
