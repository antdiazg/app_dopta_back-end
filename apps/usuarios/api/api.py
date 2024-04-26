from rest_framework import generics
from apps.usuarios.models import Persona, Organizacion, Administrador
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from apps.usuarios.api.serializers import (
    PersonaSerializer,
    OrganizacionSerializer,
    AdministradorSerializer,
)


# login?
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Verificar credenciales en Persona
        try:
            user = Persona.objects.get(username=username)
        except Persona.DoesNotExist:
            # Verificar credenciales en Organizacion
            try:
                user = Organizacion.objects.get(username=username)
            except Organizacion.DoesNotExist:
                # Verificar credenciales en Administrador
                try:
                    user = Administrador.objects.get(username=username)
                except Administrador.DoesNotExist:
                    return Response(
                        {"error": "El usuario no existe"}, status=status.HTTP_401_UNAUTHORIZED
                    )

        if not user.check_password(password):
            return Response(
                {"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Generar token de autenticación
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


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
