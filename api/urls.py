from django.urls import path
from .login import login, register, validar_token

urlpatterns = [
    path('login', login),
    path('register', register),
    path('validartoken', validar_token)
]
