from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

# from simple_history.models import HistoricalRecords


class PersonaManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        telefono,
        direccion,
        password,
        is_staff,
        is_superuser,
        nombre,
        apellido,
        **extra_fields,
    ):
        user = self.model(
            username=username,
            email=email,
            telefono=telefono,
            direccion=direccion,
            is_staff=is_staff,
            is_superuser=is_superuser,
            nombre=nombre,
            apellido=apellido,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
        self,
        username,
        email,
        telefono,
        direccion,
        nombre,
        apellido,
        password=None,
        **extra_fields,
    ):
        return self._create_user(
            username,
            email,
            telefono,
            direccion,
            nombre,
            apellido,
            password,
            False,
            False,
            **extra_fields,
        )


class AdminManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        telefono,
        direccion,
        password,
        is_staff,
        is_superuser,
        admin_numrut,
        admin_dv,
        admin_p_nombre,
        admin_s_nombre,
        admin_apaterno,
        admin_apmaterno,
        admin_fec_nac,
        **extra_fields,
    ):
        user = self.model(
            username=username,
            email=email,
            telefono=telefono,
            direccion=direccion,
            is_staff=is_staff,
            is_superuser=is_superuser,
            admin_numrut=admin_numrut,
            admin_dv=admin_dv,
            admin_p_nombre=admin_p_nombre,
            admin_s_nombre=admin_s_nombre,
            admin_apaterno=admin_apaterno,
            admin_apmaterno=admin_apmaterno,
            admin_fec_nac=admin_fec_nac,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(
        self,
        username,
        email,
        telefono,
        direccion,
        admin_numrut,
        admin_dv,
        admin_p_nombre,
        admin_s_nombre,
        admin_apaterno,
        admin_apmaterno,
        admin_fec_nac,
        passwerd=None,
        **extra_fields,
    ):
        return self._create_user(
            username,
            email,
            telefono,
            direccion,
            admin_numrut,
            admin_dv,
            admin_p_nombre,
            admin_s_nombre,
            admin_apaterno,
            admin_apmaterno,
            admin_fec_nac,
            passwerd,
            True,
            True,
            **extra_fields,
        )


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        "Correo Electrónico",
        max_length=255,
        unique=True,
    )
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # historical = HistoricalRecords()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.id} {self.username}"


class Persona(Usuario):
    persona_id = models.AutoField(unique=True, primary_key=True)
    nombre = models.CharField("Nombre", max_length=50)
    apellido = models.CharField("Apellido", max_length=50)
    objects = PersonaManager()

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.persona_id} {self.username}"


class Administrador(Usuario):
    admin_id = models.AutoField(unique=True, primary_key=True)
    admin_numrut = models.IntegerField("Numero de rut")
    admin_dv = models.CharField("Digito verificador", max_length=1)
    admin_p_nombre = models.CharField("Primer nombre", max_length=25)
    admin_s_nombre = models.CharField(
        "Segundo Nombre", max_length=25, blank=True, null=True
    )
    admin_apaterno = models.CharField("Apellido paterno", max_length=25)
    admin_apmaterno = models.CharField(
        "Apellido materno", max_length=25, blank=True, null=True
    )
    admin_fec_nac = models.DateField()
    objects = AdminManager()

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return f"{self.admin_id} {self.username} ({self.admin_p_nombre} {self.admin_apaterno})"
