from django.db import models
from .miembro import Miembro
from django.utils import timezone

from .asignaciones_caso import Asignaciones_caso
import datetime
from django.core.exceptions import ValidationError

class EvidenciaTarea(models.Model):
    asignacion = models.ForeignKey(Asignaciones_caso, on_delete=models.CASCADE, related_name='evidencias_tarea',blank=True, null= True)
    descripcion = models.TextField(max_length=100,blank=True, null= True)
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    archivo_evidencia = models.FileField(upload_to="media/evidencias", blank=True, null=True)
    campo_inicio = models.DateTimeField(default=timezone.now)
    fechalimite = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=100,blank=True, null= True)
    prioridades = models.CharField(max_length=100,blank=True, null= True)
    
    def __str__(self):
        return f"Evidencia proporcionada por {self.miembro} para la asignación de caso: {self.asignacion}"

    def clean(self):
        fecha_inicio = self.campo_inicio.date()  

        
        if self.fechalimite and fecha_inicio > self.fechalimite:
            raise ValidationError("La fecha límite no puede ser menor que la fecha de inicio.")
