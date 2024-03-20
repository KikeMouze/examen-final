from .asignaciones_caso import Asignaciones_caso
from django.db import models
from django.utils import timezone
from django.contrib import messages

class Audiencia(models.Model):
    caso = models.ForeignKey(Asignaciones_caso, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.plazo_critico():
            messages.warning("La fecha de la audiencia está dentro de un plazo crítico. Por favor, revísela.")
        
        super().save(*args, **kwargs)

    def plazo_critico(self):
        diferencia_dias = (self.fecha - timezone.now()).days
        return diferencia_dias <= 7  