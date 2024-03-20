from django.db import models
from django.utils import timezone
from .cliente import Cliente
from .miembro import Miembro
from .caso import Caso
import datetime
from django.core.exceptions import ValidationError

class Asignaciones_caso(models.Model):
    asignacion= models.CharField(max_length=100 , blank=True, null= True)
    clientes = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tabla_intermedia_cliente',blank=True, null= True)
    miembros = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='tabla_intermedia_miebro',blank=True, null= True)
    casos = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='tabla_intermedia_caso',blank=True, null= True)

    archivo = models.FileField(upload_to="media/uploads", blank=True, null=True)
    campo_inicio= models.DateTimeField(default=timezone.now)
    fechalimite = models.DateField(blank=True,null=True)

    
    prioridades = models.CharField(max_length=100 ,blank=True, null= True)
   
    estado = models.CharField(max_length=100, blank=True, null= True)

    def __str__(self):
        return f"{self.casos} - {self.miembros} - {self.clientes}"
    def clean(self):
        fecha_inicio = self.campo_inicio.date()  

        if self.fechalimite and fecha_inicio > self.fechalimite:
            raise ValidationError("La fecha límite no puede ser menor que la fecha de inicio.")