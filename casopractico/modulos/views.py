from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views import generic
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django import forms
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Cliente,Miembro,Caso,Asignaciones_caso,EvidenciaTarea,Audiencia

def index(request):
  
    asignaciones_caso = Asignaciones_caso.objects.all()

  
    return render(
        request,
        'index.html',
        context={'cantidadCliente': {asignaciones_caso}}
    )

@method_decorator(never_cache, name='dispatch') 
class clienteListView(generic.ListView):
   model = Cliente
   permission_required = 'modulos.add_cliente'

   paginate_by = 2


   def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(cedula__icontains=query))

        return queryset

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class clienteCreate(PermissionRequiredMixin,CreateView):
    model = Cliente
    fields = ['nombre', 'apellido','cedula','correo']
    permission_required = 'model.add_cliente'
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cliente-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class clienteDetailView(generic.DetailView):
    model = Cliente
    context_object_name = 'cliente'
    template_name = 'modulos/cliente_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        registros_tabla_intermedia = Asignaciones_caso.objects.filter(clientes=cliente)
        context['registros_tabla_intermedia'] = registros_tabla_intermedia
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class clienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'apellido','cedula','correo']
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cliente-update', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class clienteDelete(LoginRequiredMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('cliente')
    permission_required = 'modulos.delete_cliente'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            pass

@login_required
def reportes(request):
    response = render(request, 'reportes.html',)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate' 
    response['Pragma'] = 'no-cache'  
    response['Expires'] = '0'  
    return response

@login_required
def reporte_cliente(request):
    clientes = Cliente.objects.all()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_cliente.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Cliente"

    ws.append(["nombre", "apellido","cedula","correo"])

    
    for cliente in clientes:
        ws.append([
            cliente.nombre,
            cliente.apellido,
            cliente.cedula,
            cliente.correo,

            
        ])

    wb.save(response)
    return response

from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generar_pdf(request):
    cliente = Cliente.objects.first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ejemplo.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 750, "Universidad UISRAEL")
    p.drawString(100, 730, "Nombre del cliente: {}".format(cliente.nombre))
    p.drawString(100, 710, "Apellido del cliente: {}".format(cliente.apellido))
    p.drawString(100, 690, "Cédula del cliente: {}".format(cliente.cedula))
    p.drawString(100, 670, "Correo del cliente: {}".format(cliente.correo))

    p.showPage()
    p.save()

    return response


def lista_clientes(request):
    query = request.GET.get('q', '')
    nombre = request.GET.get('nombre', '')
    descripcion = request.GET.get('descripcion', '')

    clientes = Cliente.objects.all()

    nombres = clientes.values_list('nombre', flat=True).distinct()
    descripciones = clientes.values_list('descripcion', flat=True).distinct()

    if query:
        clientes = clientes.filter(nombre__icontains=query) | clientes.filter(descripcion__icontains=query)

    if nombre:
        clientes = clientes.filter(nombre=nombre)
    if descripcion:
        clientes = clientes.filter(descripcion__icontains=descripcion)

    return render(request, 'cliente_list.html', {'object_list': clientes, 'query': query, 'nombre': nombre, 'descripcion': descripcion, 'nombres': nombres, 'descripciones': descripciones})


from django.utils import timezone

def buscar_cliente(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    año = request.GET.get('año')
    if fecha_inicio and fecha_fin:
        fecha_inicio_dt = timezone.make_aware(timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d'))
        fecha_fin_dt = timezone.make_aware(timezone.datetime.strptime(fecha_fin, '%Y-%m-%d'))
        
        clientes = Cliente.objects.filter(campo_fecha__date__range=(fecha_inicio_dt.date(), fecha_fin_dt.date()))
    else:
        clientes = None
    
    if año:
        clientes = Cliente.objects.filter(campo_fecha__year=año)
    else:
        clientes = None


    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')

    if año_inicio and año_fin:
        clientes = Cliente.objects.filter(campo_fecha__year__range=(año_inicio, año_fin))
    else:
        clientes = None   

    return render(request, 'model/buscar_cliente.html', {'clientes': clientes})












@method_decorator(never_cache, name='dispatch')
class miembroListView(generic.ListView):
   model = Miembro
   permission_required = 'modulos.add_miembro'

   paginate_by = 2

   def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(cedula__icontains=query))

        return queryset

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class miembroCreate(PermissionRequiredMixin,CreateView):
    model = Miembro
    fields = ['nombre', 'apellido','cedula','correo']
    permission_required = 'model.add_miembro'
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('miembro-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class miembroDetailView(generic.DetailView):
    model = Miembro
    context_object_name = 'miembro'
    template_name = 'modulos/miembro_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        miembro = self.get_object()
        registros_tabla_intermedia = Asignaciones_caso.objects.filter(miembros=miembro)
        context['registros_tabla_intermedia'] = registros_tabla_intermedia
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class miembroUpdate(LoginRequiredMixin, UpdateView):
    model = Miembro
    fields = ['nombre', 'apellido','cedula','correo']
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('miembro-update', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class miembroDelete(LoginRequiredMixin, DeleteView):
    model = Miembro
    success_url = reverse_lazy('miembro')
    permission_required = 'modulos.delete_miembro'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            pass



        





@method_decorator(never_cache, name='dispatch')
class casoListView(generic.ListView):
   model = Caso
   permission_required = 'model.add_caso'
    
   paginate_by = 2

   def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(Q(tipo__icontains=query) | Q(id__icontains=query)|Q(detalleRelevantes__icontains=query))

        return queryset

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class casoCreate(PermissionRequiredMixin,CreateView):
    model = Caso
    fields = ['tipo', 'fechaInicio','detalleRelevantes']
    permission_required = 'model.add_caso'
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('caso-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class casoDetailView(generic.DetailView):
    model = Caso
    context_object_name = 'caso'
    template_name = 'modulos/caso_detail.html'  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)  
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class casoUpdate(LoginRequiredMixin, UpdateView):
    model = Caso
    fields = ['tipo', 'fechaInicio','detalleRelevantes']
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('caso-update', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class casoDelete(LoginRequiredMixin, DeleteView):
    model = Caso
    success_url = reverse_lazy('caso')
    permission_required = 'modulos.delete_caso'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            pass
   



        
def visualizar_persona_uno(request, cliente_id):
    persona_uno = Cliente.objects.get(pk=cliente_id)
    cantidad_registros = Asignaciones_caso.objects.filter(clientes=persona_uno).count()
    registros_tabla_intermedia = Asignaciones_caso.objects.filter(clientes=persona_uno)

    return render(request, 'visualizar_persona_cliente.html', {'persona_uno': persona_uno, 'cantidad_registros': cantidad_registros, 'registros_tabla_intermedia': registros_tabla_intermedia})


def visualizar_persona_dos(request, miembro_id):
    persona_dos = Miembro.objects.get(pk=miembro_id)
    cantidad_registros = Asignaciones_caso.objects.filter(clientes=persona_dos).count()
    return render(request, 'visualizar_persona_dos.html', {'persona_uno': persona_dos, 'cantidad_registros': cantidad_registros})




def visualizar_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(Asignaciones_caso, pk=asignacion_id)
    evidencias = asignacion.evidencias_tarea.all()
    return render(request, 'modulos/visualizar_asignacion.html', {'asignacion': asignacion, 'evidencias': evidencias})









def visualizar_asignaciones_caso(request, asignaciones_caso_id):
    asignaciones_caso = Asignaciones_caso.objects.get(pk=asignaciones_caso_id)
    cantidad_registros_persona_uno = Asignaciones_caso.objects.filter(clientes=asignaciones_caso.clientes).count()
    cantidad_registros_persona_dos = Asignaciones_caso.objects.filter(personasdos=asignaciones_caso.personasdos).count()
    return render(request, 'visualizar_asignaciones_caso.html', {'asignaciones_caso': asignaciones_caso, 'cantidad_registros_persona_uno': cantidad_registros_persona_uno, 'cantidad_registros_persona_dos': cantidad_registros_persona_dos})






# PERFIL DE UN USUARIO:



from django.http import Http404

from django.shortcuts import render
from django.http import HttpResponse

def ver_insumos_personauno(request):
    try:
        clientes = Cliente.objects.get(usuario=request.user)
        asignaciones_casos = clientes.casos.all()
        return render(request, 'ver-insumos-personauno.html', {'asignaciones_casos': asignaciones_casos})
    except Cliente.DoesNotExist:
        return HttpResponse('No se encontró ninguna PersonaUno asociada a este usuario.')






@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
def ver_tabla_intermedia(request):
    persona_uno = request.user.cliente_set.first()

    if persona_uno:
        registros_tabla_intermedia = Asignaciones_caso.objects.filter(clientes=persona_uno)

        return render(request, 'modulos/ver_tabla_intermedia.html', {'registros_tabla_intermedia': registros_tabla_intermedia})
    else:
        return render(request, 'modulos/error.html', {'mensaje': 'No se encontraron registros de tabla intermedia para esta persona.'})







@method_decorator(never_cache, name='dispatch')
class asignaciones_casoListView(generic.ListView):
   model = Asignaciones_caso
   permission_required = 'model.add_asignaciones_caso'

   paginate_by = 2

   def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(Q(id__icontains=query))

        return queryset
   

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class asignaciones_casoCreate(PermissionRequiredMixin,CreateView):
    model = Asignaciones_caso
    fields = fields = ['asignacion','clientes', 'miembros', 'casos', 'archivo', 'campo_inicio','fechalimite', 'prioridades','estado']#PONER LOS CAMPOS#
    permission_required = 'model.add_asignaciones_caso'
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('asignaciones_caso-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class asignaciones_casoDetailView(generic.DetailView):
    model = Asignaciones_caso
    context_object_name = 'asignaciones_caso'
    template_name = 'modulos/asignaciones_caso_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignacion = self.get_object()
        registros_tabla_intermedia = EvidenciaTarea.objects.filter(asignacion=asignacion)
        context['registros_tabla_intermedia'] = registros_tabla_intermedia
        return context
     
  

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class asignaciones_casoupdate(LoginRequiredMixin, UpdateView):
    model = Asignaciones_caso
    fields = fields = ['clientes', 'miembros', 'casos', 'archivo', 'campo_inicio','fechalimite', 'prioridades','estado']
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('asignaciones_caso-update', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class asignaciones_casodelete(LoginRequiredMixin, DeleteView):
    model = Asignaciones_caso
    success_url = reverse_lazy('asignaciones_caso')
    permission_required = 'modulos.delete_asignaciones_caso'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            pass
   




from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Asignaciones_caso
def descargar_archivo(request, asignacion_id):
    asignacion = get_object_or_404(Asignaciones_caso, pk=asignacion_id)
    if asignacion.archivo:
        try:
            with asignacion.archivo.open('rb') as archivo:
                response = HttpResponse(archivo.read())
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename="{asignacion.archivo.name}"'
                return response
        except FileNotFoundError:
            return HttpResponse("El archivo solicitado no se encuentra.", status=404)
    else:
        return HttpResponse("No hay archivo adjunto para esta asignación.", status=404)




@method_decorator(never_cache, name='dispatch')
class evidenciatareaListView(generic.ListView):
   model = EvidenciaTarea
   permission_required = 'model.add_evidenciaTarea'

   paginate_by = 2

   def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(Q(descripcion__icontains=query))

        return queryset
   

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class evidenciatareaCreate(PermissionRequiredMixin,CreateView):
    model = EvidenciaTarea
    fields = fields = ['asignacion','descripcion', 'miembro', 'archivo_evidencia', 'campo_inicio','fechalimite', 'estado','prioridades']#PONER LOS CAMPOS#   
    permission_required = 'model.add_evidenciaTarea'
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('evidenciatarea-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class evidenciatareaDetailView(generic.DetailView):
    model = EvidenciaTarea
    context_object_name = 'evidenciaTarea'
    template_name = 'modulos/evidenciaTarea_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)  
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class evidenciatareaupdate(LoginRequiredMixin, UpdateView):
    model = EvidenciaTarea
    fields = fields = ['asignacion','descripcion', 'miembro', 'archivo_evidencia', 'campo_inicio','fechalimite', 'estado','prioridades']    # Método opcional para agregar lógica adicional antes de guardar el formulario
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('evidenciatarea-update', kwargs={'pk': self.object.pk})









@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class evidenciatareadelete(LoginRequiredMixin, DeleteView):
    model = EvidenciaTarea
    success_url = reverse_lazy('evidenciatarea')
    permission_required = 'modulos.delete_evidenciatarea'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            pass


from django.shortcuts import get_object_or_404, HttpResponse
from .models import EvidenciaTarea


def descargar_archivo_evidencia(request, evidenciatarea_id):
    evidenciatarea = get_object_or_404(EvidenciaTarea, pk=evidenciatarea_id)
    if evidenciatarea.archivo_evidencia:
        try:
            with evidenciatarea.archivo_evidencia.open('rb') as archivo:
                response = HttpResponse(archivo.read())
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename="{evidenciatarea.archivo_evidencia.name}"'
                return response
        except FileNotFoundError:
            return HttpResponse("El archivo solicitado no se encuentra.", status=404)
    else:
        return HttpResponse("No hay archivo adjunto para esta tarea.", status=404)
def descargar_archivo_evidencia_asignacion(request, evidencia_id):
    evidencia = get_object_or_404(EvidenciaTarea, pk=evidencia_id)
    if evidencia.archivo_evidencia:
        try:
            with evidencia.archivo_evidencia.open('rb') as archivo:
                response = HttpResponse(archivo.read())
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename="{evidencia.archivo_evidencia.name}"'
                return response
        except FileNotFoundError:
            return HttpResponse("El archivo solicitado no se encuentra.", status=404)
    else:
        return HttpResponse("No hay archivo adjunto para esta evidencia.", status=404)
    



from django.db.models.functions import ExtractYear

from django.db.models import Q

from datetime import datetime

class audienciaListView(generic.ListView):
    model = Audiencia
    paginate_by = 2
 

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(Q(fecha__icontains=query))

        return queryset

   

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class audienciaCreate(PermissionRequiredMixin,CreateView):
    model = Audiencia
    fields = fields = ['caso','fecha']      
    permission_required = 'model.add_audiencia'
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('audiencia-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class audienciaDetailView(generic.DetailView):
    model = Audiencia
    context_object_name = 'audiencia'
    template_name = 'modulos/audiencia_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)  
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class audienciaupdate(LoginRequiredMixin, UpdateView):
    model = Audiencia
    fields = fields = ['caso','fecha']    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('audiencia-update', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class audienciadelete(LoginRequiredMixin, DeleteView):
    model = Audiencia
    success_url = reverse_lazy('audiencia')
    permission_required = 'modulos.delete_audiencia'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            pass



@login_required
def calendario(request):
    response = render(request, 'calendario.html',)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate' 
    response['Pragma'] = 'no-cache'  
    response['Expires'] = '0'  
    return response


