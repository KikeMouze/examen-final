from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
#from .views import generar_pdf
from .views import descargar_archivo,descargar_archivo_evidencia,descargar_archivo_evidencia_asignacion



urlpatterns = [
    path('', views.index, name='index'),

    path('cliente/',login_required(views.clienteListView.as_view()), name='cliente'),
    path('cliente/create/', login_required(views.clienteCreate.as_view()), name='cliente-create'),
    path('cliente/<int:pk>/', login_required(views.clienteDetailView.as_view()), name='cliente-detail'),
    path('cliente/<int:pk>/update/', login_required(views.clienteUpdate.as_view()), name='cliente-update'),
    path('cliente/<int:pk>/delete/', login_required(views.clienteDelete.as_view()), name='cliente-delete'),
    
    path('miembro/',login_required(views.miembroListView.as_view()), name='miembro'),
    path('miembro/create/', login_required(views.miembroCreate.as_view()), name='miembro-create'),
    path('miembro/<int:pk>/', login_required(views.miembroDetailView.as_view()), name='miembro-detail'),
    path('miembro/<int:pk>/update/', login_required(views.miembroUpdate.as_view()), name='miembro-update'),
    path('miembro/<int:pk>/delete/', login_required(views.miembroDelete.as_view()), name='miembro-delete'),
    
    
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/cliente/', views.reporte_cliente, name='reporte_cliente'),

    
    path('caso/',login_required(views.casoListView.as_view()), name='caso'),
    path('caso/create/', login_required(views.casoCreate.as_view()), name='caso-create'),
    path('caso/<int:pk>/', login_required(views.casoDetailView.as_view()), name='caso-detail'),
    path('caso/<int:pk>/update/', login_required(views.casoUpdate.as_view()), name='caso-update'),
    path('caso/<int:pk>/delete/', login_required(views.casoDelete.as_view()), name='caso-delete'),

    path('asignaciones_caso/',login_required(views.asignaciones_casoListView.as_view()), name='asignaciones_caso'),
    path('asignaciones_caso/create/', login_required(views.asignaciones_casoCreate.as_view()), name='asignaciones_caso-create'),
    path('asignaciones_caso/<int:pk>/', login_required(views.asignaciones_casoDetailView.as_view()), name='asignaciones_caso-detail'),
    path('asignaciones_caso/<int:pk>/update/', login_required(views.asignaciones_casoupdate.as_view()), name='asignaciones_caso-update'),
    path('asignaciones_caso/<int:pk>/delete/', login_required(views.asignaciones_casodelete.as_view()), name='asignaciones_caso-delete'),

    path('evidenciatarea/',login_required(views.evidenciatareaListView.as_view()), name='evidenciatarea'),
    path('evidenciatarea/create/', login_required(views.evidenciatareaCreate.as_view()), name='evidenciatarea-create'),
    path('evidenciatarea/<int:pk>/', login_required(views.evidenciatareaDetailView.as_view()), name='evidenciatarea-detail'),
    path('evidenciatarea/<int:pk>/update/', login_required(views.evidenciatareaupdate.as_view()), name='evidenciatarea-update'),
    path('evidenciatarea/<int:pk>/delete/', login_required(views.evidenciatareadelete.as_view()), name='evidenciatarea-delete'),


    path('audiencia/',login_required(views.audienciaListView.as_view()), name='audiencia'),
    path('audiencia/create/', login_required(views.audienciaCreate.as_view()), name='audiencia-create'),
    path('audiencia/<int:pk>/', login_required(views.audienciaDetailView.as_view()), name='audiencia-detail'),
    path('audiencia/<int:pk>/update/', login_required(views.audienciaupdate.as_view()), name='audiencia-update'),
    path('audiencia/<int:pk>/delete/', login_required(views.audienciadelete.as_view()), name='audiencia-delete'),





    path('cliente/<int:cliente_id>/', views.visualizar_persona_uno, name='visualizar_persona_uno'),
    path('miembro/<int:miembro_id>/', views.visualizar_persona_dos, name='visualizar_persona_dos'),
    path('asignaciones_caso/<int:asignacion_id>/', views.visualizar_asignacion, name='visualizar_asignacion'),





    path('ver_tabla_intermedia/', views.ver_tabla_intermedia, name='ver_tabla_intermedia'),

    #path('ver_asignaciones_caso_personauno/', views.ver_asignaciones_caso_personauno, name='ver-asignaciones_caso-personauno'),
    path('ver_insumos_personauno/', views.ver_insumos_personauno, name='ver-insumos-personauno'),

    path('descargar/<int:asignacion_id>/', descargar_archivo, name='descargar_archivo'),
    path('modulos/evidenciatarea/<int:evidenciatarea_id>/descargar/', descargar_archivo_evidencia, name='descargar_archivo_evidencia'),
    path('descargar_evidencia/<int:evidencia_id>/', descargar_archivo_evidencia_asignacion, name='descargar_evidencia_asignacion'),
    path('calendario/', views.calendario, name='calendario'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)