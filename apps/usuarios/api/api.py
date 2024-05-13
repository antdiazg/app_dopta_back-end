from django.conf import settings
from django.apps import apps
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.usuarios.models import Persona, Organizacion, Administrador
from apps.usuarios.api.serializers import (
    PersonaSerializer,
    OrganizacionSerializer,
    AdministradorSerializer,
    LoginSerializer,
    RecuPassConfirmacionSerializer,
    RecuPassSolicitudSerializer,
)

""" TODO:
    - Eliminar vistas innecesarias
    - recuperacion de contraseñas
"""


# login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            # Autenticar el usuario en cada uno de los modelos de usuario personalizados
            clases = [Persona, Organizacion, Administrador]
            for clase in clases:
                user = self.authenticate_user(clase, username, password)
                if user:
                    if user.is_active:
                        user.last_login = timezone.now()
                        user.save(update_fields=["last_login"])
                        # Generar token JWT
                        refresh = RefreshToken.for_user(user)
                        return Response(
                            {
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        # Generar token de activación
                        token = default_token_generator.make_token(user)
                        activation_link = (
                            settings.BASE_URL
                            + reverse("activate-account")
                            + f"?email={user.email}&token={token}&user_type={clase.__name__}"
                        )
                        subject = "Activación de cuenta"
                        message = f"Por favor, haz clic en el siguiente enlace para activar tu cuenta: {activation_link}"
                        send_mail(
                            subject, message, settings.EMAIL_HOST_USER, [user.email]
                        )
                        return Response(
                            {
                                "error": "La cuenta está desactivada, se reenviara un correo con el nuevo link de actualizacion"
                            },
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    return Response(
                        {"error": "Credenciales inválidas"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        else:
            # Las credenciales son inválidas o el usuario no se encontró en ninguno de los modelos
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def authenticate_user(self, clase, username, password):
        try:
            user = clase.objects.get(username=username)
            if user.check_password(password):
                return user
        except clase.DoesNotExist:
            pass

        return None


# Persona
class PersonaListCreate(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class RegistroPersona(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generar token de activación
            token = default_token_generator.make_token(user)
            activation_link = (
                settings.BASE_URL
                + reverse("activate-account")
                + f"?email={user.email}&token={token}&user_type=Persona"
            )
            subject = "Activación de cuenta"
            message = f"Por favor, haz clic en el siguiente enlace para activar tu cuenta: {activation_link}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            return Response(
                {
                    "message": "Se ha enviado un correo electrónico de activación. Por favor, verifica tu bandeja de entrada."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Organizacion
class OrgListCreate(generics.ListCreateAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


class OrgRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


class RegistroOrganizacion(APIView):
    permission_classes = []

    def post(self, request):
        serializer = OrganizacionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generar token de activación
            token = default_token_generator.make_token(user)
            activation_link = (
                settings.BASE_URL
                + reverse("activate-account")
                + f"?email={user.email}&token={token}&user_type=Organizacion"
            )
            subject = "Activación de cuenta"
            message = f"Por favor, haz clic en el siguiente enlace para activar tu cuenta: {activation_link}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            return Response(
                {
                    "message": "Se ha enviado un correo electrónico de activación. Por favor, verifica tu bandeja de entrada."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Administrador
class AdminListCreate(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class AdminRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class ActivateAccount(APIView):
    permission_classes = []

    def get(self, request):
        email = request.GET.get("email")
        token = request.GET.get("token")
        user_type = request.GET.get("user_type")

        # Obtener el modelo de usuario correspondiente
        user_model = self.get_user_model(user_type)

        # Verificar el token y activar la cuenta
        try:
            user = user_model.objects.get(email=email)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {"message": "¡Tu cuenta ha sido activada correctamente!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Token de activación inválido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except user_model.DoesNotExist:
            return Response(
                {"error": "No se encontró ningún usuario con ese correo electrónico."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_user_model(self, user_type):
        # Mapa de modelos de usuario por tipo
        user_type_map = {
            "Persona": "usuarios.Persona",
            "Organizacion": "usuarios.Organizacion",
            "Administrador": "usuarios.Administrador",
        }

        # Obtener el nombre completo del modelo de usuario
        model_name = user_type_map.get(user_type)

        # Obtener el modelo de usuario a partir del nombre completo
        user_model = apps.get_model(model_name)

        return user_model


class RecuperarContraseñaSolicitud(APIView):
    def post(self, request):
        serializer = RecuPassSolicitudSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = self.get_user(email)
            if user:
                token = default_token_generator.make_token(user)
                reset_url = reverse("password_reset_confirm")
                reset_url += (
                    f"?email={email}&token={token}&model={user.__class__.__name__}"
                )
                reset_link = settings.BASE_URL + reset_url
                subject = "Recuperación de Contraseña"
                message = f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                return Response(
                    {
                        "message": "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": "No se encontró ningún usuario con ese correo electrónico."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user(self, email):
        users = [Persona, Organizacion, Administrador]
        for user_model in users:
            user = user_model.objects.filter(email=email).first()
            if user:
                return user
        return None


class RecuperarContraseñaConfirmacion(APIView):
    def post(self, request):
        serializer = RecuPassConfirmacionSerializer(data=request.data)
        if serializer.is_valid():
            email = request.GET.get("email")
            token = request.GET.get("token")
            user_type = request.GET.get("model")
            new_password = serializer.validated_data["new_password"]
            try:
                user = self.get_user(email, user_type)
                if user and default_token_generator.check_token(user, token):

                    user.password = new_password
                    user.save()
                    return Response(
                        {"message": "La contraseña se ha restablecido correctamente."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Token de restablecimiento de contraseña inválido."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except:
                return Response({"error": "Link invalido!!!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user(self, email, user_type):
        if user_type == "Persona":
            return Persona.objects.filter(email=email).first()
        elif user_type == "Organizacion":
            return Organizacion.objects.filter(email=email).first()
        elif user_type == "Administrador":
            return Administrador.objects.filter(email=email).first()
        else:
            return None
