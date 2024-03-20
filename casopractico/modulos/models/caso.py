from django.db import models
from django.utils import timezone

class Caso(models.Model):
    tipo = models.CharField(max_length=100) 
    fechaInicio = models.DateTimeField(default=timezone.now)
    detalleRelevantes=models.TextField(blank=True, null= True)

    def __str__(self):
        return self.tipo