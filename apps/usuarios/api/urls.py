from django.urls import path
from apps.usuarios.api.api import (
    PersonaListCreate,
    PersonaRetrieveUpdateDestroy,
    OrgListCreate,
    OrgRetrieveUpdateDestroy,
    AdminListCreate,
    AdminRetrieveUpdateDestroy,
    LoginView,
    RegistroPersona,
    RegistroOrganizacion,
    ActivateAccount,
    RecuperarContraseñaConfirmacion,
    RecuperarContraseñaSolicitud,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("personas/", PersonaListCreate.as_view(), name="persona-list-create"),
    path(
        "personas/<int:pk>/",
        PersonaRetrieveUpdateDestroy.as_view(),
        name="persona-retrieve-update-destroy",
    ),
    path("organizacion/", OrgListCreate.as_view(), name="organizacion-list-create"),
    path(
        "organizacion/<int:pk>/",
        OrgRetrieveUpdateDestroy.as_view(),
        name="organizacion-retrieve-update-destroy",
    ),
    path("administrador/", AdminListCreate.as_view(), name="administrador-list-create"),
    path(
        "administrador/<int:pk>/",
        AdminRetrieveUpdateDestroy.as_view(),
        name="administrador-retrieve-update-destroy",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("personas/registro/", RegistroPersona.as_view(), name="registro-persona"),
    path("organizacion/registro/", RegistroOrganizacion.as_view(), name="registro-org"),
    path("activate-account/", ActivateAccount.as_view(), name="activate-account"),
    path(
        "password/reset/",
        RecuperarContraseñaSolicitud.as_view(),
        name="password_reset_request",
    ),
    path(
        "password/reset/confirm/",
        RecuperarContraseñaConfirmacion.as_view(),
        name="password_reset_confirm",
    ),
]
