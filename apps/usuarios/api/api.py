import uuid
from rest_framework.decorators import api_view
from rest_framework import generics
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from apps.usuarios.models import Persona, Organizacion, Administrador, CustomToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from apps.usuarios.api.serializers import (
    PersonaSerializer,
    OrganizacionSerializer,
    AdministradorSerializer,
    LoginSerializer,
)


# login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            # Autenticar el usuario en cada uno de los modelos de usuario personalizados
            user_types = [Persona, Organizacion, Administrador]
            for user_type in user_types:
                user = self.authenticate_user(user_type, username, password)
                if user:
                    token = self.generate_token(user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK)

        # Las credenciales son inválidas o el usuario no se encontró en ninguno de los modelos
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

    def authenticate_user(self, user_type, username, password):
        try:
            user = user_type.objects.get(username=username)
            if user.check_password(password):
                return user
        except user_type.DoesNotExist:
            pass
        
        return None

    def generate_token(self, user):
        # Verificar si el usuario ya tiene un token asignado
        token = CustomToken.objects.filter(user_id=user.id).first()
        if token:
            return token
        
        # Generar un valor único para la clave key
        token_key = str(uuid.uuid4())
        
        # Si no tiene un token asignado, creamos uno nuevo con la clave key generada
        new_token = CustomToken.objects.create(user_id=user.id, key=token_key)
        return new_token


# Persona
class PersonaListCreate(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


# Organizacion
class OrgListCreate(generics.ListCreateAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


class OrgRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


# Administrador
class AdminListCreate(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class AdminRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
