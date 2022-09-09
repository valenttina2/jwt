from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

class RegisterView(APIView):
    def post(self, request):
        if (request.method == 'POST'):
            serializer=UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if User is None:
            raise AuthenticationFailed('Пользователь не найден')

        # if not user.check_password(password):
        #     raise AuthenticationFailed('Неверный пароль')

        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=500),
            'iat':datetime.datetime.utcnow()
        }

        token=jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response=Response()
        response.set_cookie(key='jwt',
                            value=token,
                            httponly=True
                            )
        response.data={
                'jwt':token
                }

        return response

class UserView(APIView):
    def get(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Не прошeдший проверку подлинности')

        try:
            payload=jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Не прошeдший проверку подлинности')

        user = User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)

        return Response(serializer.data)

class Logaut(APIView):
    def post(self, request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'messege':'успешно'
        }

        return response

