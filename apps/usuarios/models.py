from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Usuario(models.Model):
    username = models.CharField(max_length=255, unique=True)
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


class Persona(Usuario):
    id_per = models.AutoField(unique=True, primary_key=True)
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


# oli
@receiver(post_save, sender=Persona)
@receiver(post_save, sender=Organizacion)
@receiver(post_save, sender=Administrador)
def crear_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(
            username=instance.username,
            email=instance.email,
            telefono=instance.telefono,
            direccion=instance.direccion,
            is_active=instance.is_active,
            is_staff=instance.is_staff,
        )
