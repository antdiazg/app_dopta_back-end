from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.usuarios.models import Usuario, Persona, Administrador
from apps.usuarios.api.serializers import (
    AdministradorSerializer,
    PersonaSerializer,
    UsuarioSerializer,
)

# Usuario


@api_view(["GET"])
def usuario_api_view(request):

    if request.method == "GET":
        usuarios = Usuario.objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return Response(usuarios_serializer.data)


@api_view(["GET"])
def usuario_detail_api_view(request, pk=None):

    if request.method == "GET":
        usuario = Usuario.objects.filter(id=pk).first()
        usuario_serializer = UsuarioSerializer(usuario)
        return Response(usuario_serializer.data)


# Persona


@api_view(["GET"])
def persona_api_view(request):

    if request.method == "GET":
        personas = Persona.objects.all()
        personas_serializer = PersonaSerializer(personas, many=True)
        return Response(personas_serializer.data)


@api_view(["GET"])
def persona_detail_api_view(request, pk=None):

    if request.method == "GET":
        persona = Persona.objects.filter(id=pk).first()
        persona_serializer = PersonaSerializer(persona)
        return Response(persona_serializer.data)


# admin


@api_view(["GET"])
def admin_api_view(request):

    if request.method == "GET":
        administradores = Administrador.objects.all()
        administradores_serializer = AdministradorSerializer(administradores, many=True)
        return Response(administradores_serializer.data)


@api_view(["GET"])
def admin_detail_api_view(request, pk=None):

    if request.method == "GET":
        administrador = Administrador.objects.filter(id=pk).first()
        administrador_serializer = AdministradorSerializer(administrador)
        return Response(administrador_serializer.data)
