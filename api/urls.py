from django.urls import path
from .login import login, validar_token

urlpatterns = [
    path('login', login),
    path('validartoken', validar_token)
]
