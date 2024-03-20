from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from modulos import views  # Importa la vista index desde catalog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('modulos/', include('modulos.urls')),
    path('accounts/', RedirectView.as_view(url='/login')),  # Redirige la página de inicio a '/' al iniciar sesión
    path('', views.index, name='index'),  # Ruta para cargar la página de inicio
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
