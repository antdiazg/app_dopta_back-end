from django.urls import path
from apps.usuarios.api.api import (
    PersonaListCreate,
    PersonaRetrieveUpdateDestroy,
    OrgListCreate,
    OrgRetrieveUpdateDestroy,
    AdminListCreate,
    AdminRetrieveUpdateDestroy,
)

urlpatterns = [
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
    # Repite el mismo patrón para Organizacion y Administrador
]
