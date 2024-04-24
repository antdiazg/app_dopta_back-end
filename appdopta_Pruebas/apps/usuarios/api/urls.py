from django.urls import path
from apps.usuarios.api.api import (
    usuario_api_view,
    usuario_detail_api_view,
    persona_api_view,
    persona_detail_api_view,
    admin_api_view,
    admin_detail_api_view,
)

urlpatterns = [
    path("usuario/", usuario_api_view, name="usuario_api"),
    path("usuario/<int:pk>/", usuario_detail_api_view, name="usuario_detail_api_view"),
    path("persona/", persona_api_view, name="persona_api"),
    path("persona/<int:pk>/", persona_detail_api_view, name="persona_detail_api_view"),
    path("administrador/", admin_api_view, name="admin_api"),
    path(
        "administrador/<int:pk>/", admin_detail_api_view, name="admin_detail_api_view"
    ),
]
