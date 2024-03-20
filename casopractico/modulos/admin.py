from django.contrib import admin

from .models import Cliente,Miembro,Asignaciones_caso,Caso
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CasoResource(resources.ModelResource):
    class Meta:
        model=Caso
class CasoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['tipo','fechaInicio', 'detalleRelevantes']
    resource_class=CasoResource  
admin.site.register(Caso, CasoAdmin)
class ClienteResource(resources.ModelResource):
    class Meta:
        model=Cliente
class ClienteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['nombre','apellido', 'cedula','correo','campo_fecha']
    resource_class=ClienteResource  
admin.site.register(Cliente, ClienteAdmin)



class MiembroResource(resources.ModelResource):
    class Meta:
        model=Miembro
class MiembroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['nombre','apellido', 'cedula','correo', 'campo_fecha']
    resource=MiembroResource
admin.site.register(Miembro, MiembroAdmin)

class Asignaciones_casoResource(resources.ModelResource):
    class Meta:
        model=Asignaciones_caso
class Asignaciones_casoAdmin(admin.ModelAdmin):
    list_display = ['miembros', 'clientes', 'archivo', 'campo_inicio','prioridades']
    search_fields = ['miembros__nombre', 'clientes__nombre']  
    resource_class=Asignaciones_casoResource
admin.site.register(Asignaciones_caso, Asignaciones_casoAdmin)
