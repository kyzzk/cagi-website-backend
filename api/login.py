import datetime

import jwt
import json

from env import TOKEN_SECRET
from utils.crypto import encrypt, decrypt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.usuario.models import Usuario

from django.forms.models import model_to_dict


def user_to_dict(user):
    data = {}
    for field in user._meta.fields:
        value = getattr(user, field.name)
        if not (field.name == 'foto_perfil' and not value):
            if field.name not in ['codigo_recuperacao', 'last_login', 'updated_at'] or field.name == 'created_at':
                data[field.name] = value
    return data


@api_view(['POST'])
def register(request):
    nome = request.data.get('nome')
    password = request.data.get('password')
    email = request.data.get('email')
    telefone = request.data.get('telefone')

    if not nome or not password or not email:
        return Response(status=400, data={'erro': "Por favor, forneça nome, e-mail e senha."})

    try:
        Usuario.objects.get(email=email)
        return Response(status=400, data={"erro": "Já existe um usuário com este e-mail."})
    except:
        pass

    try:
        encrypted_password = encrypt(password)
        new_user = Usuario(nome=nome, hash_password=encrypted_password, email=email, telefone=telefone, last_login=datetime.datetime.now(), foto_perfil=None)
        new_user.full_clean()
        new_user.save()

        data = user_to_dict(new_user)
        return Response(status=201, data=data)
    except Exception as e:
        return Response(status=400, data={"erro": str(e)})


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(status=400, data={'erro': "Por favor, forneça um e-mail e senha."})

    try:
        find = Usuario.objects.get(email=email)

        if decrypt(find.hash_password) == password:
            data = json.dumps(model_to_dict(find, fields=[field.name for field in find._meta.fields]), indent=4,
                              sort_keys=True, default=str)
            data = json.loads(data)
            payload = {
                "user_id": find.id,
                "email": find.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=2)
            }
            encode_jwt = jwt.encode(data, TOKEN_SECRET, algorithm='HS256')

            response_data = {
                "nome": find.nome,
                "exp": payload["exp"],
                "token": encode_jwt
            }
            return Response(response_data)
        return Response(status=401, data={"erro": "Usuário ou senha inválido."})
    except:
        return Response(status=401, data={"erro": "Usuário ou senha inválido."})


@api_view(['GET'])
def validar_token(request):
    token = request.data.get('token')

    if not token:
        return Response(status=400, data={'error': "Por favor, forneça um token."})

    try:
        jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
        return Response(status=200, data={'message': 'Token válido.'})
    except jwt.ExpiredSignatureError:
        return Response(status=401, data={'error': 'Token expirado.'})
    except jwt.InvalidTokenError:
        return Response(status=401, data={'error': 'Token inválido.'})
