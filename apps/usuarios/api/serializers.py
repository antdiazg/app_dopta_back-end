from rest_framework import serializers
from apps.usuarios.models import Persona, Organizacion, Administrador


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = "__all__"


class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = "__all__"

class RecuPassSolicitudSerializer(serializers.Serializer):
    email = serializers.EmailField()

class RecuPassConfirmacionSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data