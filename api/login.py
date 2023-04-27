import datetime

import jwt
import json

from env import TOKEN_SECRET
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.usuario.models import Usuario


from django.forms.models import model_to_dict


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(status=400, data={'erro': "Por favor, forneça um e-mail e senha."})

    try:
        find = Usuario.objects.get(email=email, hash_password=password)
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
    except:
        return Response(status=401, data={"erro": "Usuário ou senha inválido."})


@api_view(['POST'])
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
