from django.db import models
from django.utils import timezone
from .caso import Caso
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
class Miembro(models.Model):
    nombre = models.CharField(max_length=100,blank=True, null= True)
    apellido = models.CharField(max_length=100,blank=True, null= True)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(blank=True)
    campo_fecha = models.DateTimeField(default=timezone.now)
    casos = models.ManyToManyField('Caso', through='Asignaciones_caso', blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
@receiver(post_save, sender=Miembro)
def crear_usuario_cliente_dos(sender, instance, created, **kwargs):
    if created:
        username = instance.cedula  
        password = instance.cedula  
        user = User.objects.create_user(
            username=username,
            email=instance.correo,
            password=password,
            first_name=instance.nombre,
            last_name=instance.apellido,
        )
       
        group, created = Group.objects.get_or_create(name='Miembro')
        user.groups.add(group)
    
        instance.usuario = user
        instance.save()
