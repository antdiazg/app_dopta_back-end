from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.usuarios.models import Persona, Organizacion, Administrador
from apps.usuarios.api.serializers import (
    PersonaSerializer,
    OrganizacionSerializer,
    AdministradorSerializer,
    LoginSerializer,
)


# login
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data.get("username")
#             password = serializer.validated_data.get("password")

#             # Autenticar el usuario en cada uno de los modelos de usuario personalizados
#             clases = [Persona, Organizacion, Administrador]
#             for clase in clases:
#                 user = self.authenticate_user(clase, username, password)
#                 if user:
#                     print("Encontrado", user.username, clase)
#                     token = self.generate_token(user, clase)
#                     return Response({"token": token.key}, status=status.HTTP_200_OK)

#         # Las credenciales son inválidas o el usuario no se encontró en ninguno de los modelos
#         return Response(
#             {"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED
#         )

#     def authenticate_user(self, clase, username, password):
#         try:
#             user = clase.objects.get(username=username)
#             if user.check_password(password):
#                 return user
#         except clase.DoesNotExist:
#             pass

#         return None

#     def generate_token(self, user, clase):

#         # Verificar si el usuario ya tiene un token asignado
#         token = CustomToken.objects.filter(user_id=user.id, clase_usuario=clase).first()
#         if token is not None:
#             return token

#         else:
#             # Generar un hash único basado en el ID del usuario y el nombre del modelo
#             token_key = make_password(
#                 f"{user.id}-{type(user).__name__}"
#             )  # Si no tiene un token asignado, creamos uno nuevo con la clave key generada
#             new_token = CustomToken.objects.create(
#                 user_id=user.id, key=token_key, clase_usuario=clase.__name__
#             )
#             return new_token


# Persona
class PersonaListCreate(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


# class RegistroPersona(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         clase = Persona
#         ser_class = PersonaSerializer
#         serializer = ser_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()

#             # # Generar token de actualización
#             refresh = RefreshToken.for_user(user)

#             # Codificar el token para usarlo en el enlace
#             encoded_token = str(refresh)

#             # Crear el enlace para activar la cuenta
#             activation_link = reverse('activate-account') + f'?token={encoded_token}'


#             # Enviar correo de confirmación
#             subject = "Confirmación de Registro"
#             message = f"¡Gracias por registrarte! Haz clic en el siguiente enlace para activar tu cuenta:\n {activation_link}"
#             from_email = settings.EMAIL_HOST_USER
#             to_email = user.email
#             send_mail(subject, message, from_email, [to_email])

#             return Response(
#                 {
#                     "message": "Usuario registrado exitosamente. Por favor, verifica tu correo electrónico para confirmar tu registro."
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         # Manejar la solicitud GET
#         return Response(
#             {"message": "Método GET no permitido para esta vista."},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#         )

# def activate_account(request,clase):
#     if request.method == 'GET':
#         uidb64 = request.GET.get('uid')
#         token = request.GET.get('token')

#         if uidb64 and token:
#             try:
#                 user_id = urlsafe_base64_decode(uidb64)
#                 user_model = clase()
#                 user = user_model.objects.get(pk=user_id)

#                 if default_token_generator.check_token(user, token):
#                     # Activar la cuenta del usuario
#                     user.is_active = True
#                     user.save()

#                     # Mensaje de éxito
#                     messages.success(request, '¡Tu cuenta ha sido activada! Puedes iniciar sesión ahora.')
#                     return redirect(reverse('login'))
#             except Exception as e:
#                 # Mensaje de error
#                 messages.error(request, 'El enlace de activación es inválido.')
#                 return redirect(reverse('login'))

#     # Si falta el uid o el token en la solicitud o si es un método POST, redirigir al inicio de sesión
#     return redirect(reverse('login'))


class RegistroPersona(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generar token de activación
            token = default_token_generator.make_token(user)

            # Enviar correo de activación
            activation_link = (
                settings.BASE_URL
                + reverse("activate-account", args=["Persona"])
                + f"?email={user.email}&token={token}"
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


class ActivateAccount(APIView):
    permission_classes = []

    def get(self, request, user_type):
        email = request.GET.get("email")
        token = request.GET.get("token")

        # Verificar el token y activar la cuenta
        try:
            user = Persona.objects.get(email=email)
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
        except Persona.DoesNotExist:
            return Response(
                {"error": "No se encontró ningún usuario con ese correo electrónico."},
                status=status.HTTP_404_NOT_FOUND,
            )


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
