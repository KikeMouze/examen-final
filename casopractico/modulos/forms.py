

from django import forms
from models import Cliente,Miembro,Caso,Asignaciones_caso,EvidenciaTarea,Audiencia
class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombre','apellido','cedula','correo','campo_fecha','casos']

class MiembroForm(forms.ModelForm):
    class Meta:
        model=Miembro
        fields=['nombre','apellido','cedula','correo','campo_fecha','casos']


class CasoForm(forms.ModelForm):
    class Meta:
        model=Caso
        fields=['tipo','fechaInicio','detalleRelevantes']
class AudienciaForm(forms.ModelForm):
    class Meta:
        model=Caso
        fields=['caso','fecha','plazo_critico']

class Asignaciones_casoForm(forms.ModelForm):
    class Meta:
        model = Asignaciones_caso
        fields = ['asignacion','clientes', 'miembros', 'casos', 'archivo', 'campo_inicio','fechalimite','prioridades','estado']

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        return archivo


class EvidenciaTareaForm(forms.ModelForm):
    class Meta:
        model = EvidenciaTarea
        fields = ['asignacion','descripcion', 'miembro', 'archivo_evidencia', 'campo_inicio', 'fechalimite', 'estado', 'prioridades']
       

    def clean_archivo_evidencia(self):
        archivo_evidencia = self.cleaned_data['archivo_evidencia']
        return archivo_evidencia
