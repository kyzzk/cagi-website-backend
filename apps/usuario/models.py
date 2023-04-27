from django.db import models
from django_resized import ResizedImageField
from django.utils.html import format_html

from uuid import uuid4

import socket
import os


def path_and_rename(instance, filename):
    upload_to = 'static/profile_pictures'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Usuario(models.Model):
    nome = models.CharField(max_length=250, verbose_name="Nome", blank=False, null=False)
    hash_password = models.CharField(max_length=500, verbose_name="Senha em Hash", blank=True, null=True)
    email = models.CharField(max_length=250, verbose_name="E-mail", blank=True, null=True)
    telefone = models.CharField(max_length=30, verbose_name="Telefone", blank=True, null=True)
    foto_perfil = ResizedImageField(verbose_name="Upload Imagem", size=[300, 300], upload_to=path_and_rename, blank=True, null=True)
    codigo_recuperacao = models.CharField(max_length=5, verbose_name="Código de Recuperação", blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=False, verbose_name="Último Login Em")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado Em")

    def foto_de_perfil(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        if ip_address == "192.168.1.5":
            base_url = "http://127.0.0.1:8000"
        else:
            base_url = "https://cagi-backend-api.onrender.com"

        if self.foto_perfil:
            return format_html(f'<img style="width=100px;height:100px;" src="{base_url}/{self.foto_perfil}"/>')
        else:
            return format_html('<p>Sem imagem de Perfil</>')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"


