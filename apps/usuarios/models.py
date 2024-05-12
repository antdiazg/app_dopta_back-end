from django.db import models
from django.contrib.auth.hashers import check_password as check_pass_user
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField("Correo Electrónico", max_length=255, unique=True)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UsuarioManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Encriptar la contraseña antes de guardar el usuario
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_pass_user(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True


# class CustomToken(models.Model):
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#     user_id = models.IntegerField(_("User ID"))
#     clase_usuario = models.CharField(_("Nombre de clase"), max_length=50)
#     created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

#     class Meta:
#         verbose_name = _("Custom Token")
#         verbose_name_plural = _("Custom Tokens")

#     def __str__(self):
#         return self.key


class Persona(Usuario):
    nombre = models.CharField("Nombre", max_length=50)
    apellido = models.CharField("Apellido", max_length=50)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


class Organizacion(Usuario):
    rut_emp = models.IntegerField()
    razon_social = models.CharField("Razon social", max_length=50)
    telefono2 = models.IntegerField()

    class Meta:
        verbose_name = "Organizacion"
        verbose_name_plural = "Organizaciones"


class Administrador(Usuario):
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

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
