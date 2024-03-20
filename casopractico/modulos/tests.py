"""
from django.test import TestCase
from .models import Departamento

class DepartamentoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuración inicial de objetos que se utilizan en todas las pruebas del conjunto de pruebas
        Departamento.objects.create(nombre='Departamento de Prueba', descripcion='Este es un departamento de prueba')

    def test_nombre_max_length(self):
        departamento = Departamento.objects.get(id=1)
        max_length = departamento._meta.get_field('nombre').max_length
        self.assertEquals(max_length, 100)
    def test_descripcion_es_longtext(self):
        departamento = Departamento.objects.get(id=1)
        self.assertIsInstance(departamento.descripcion, str)
   
    def test_archivo_max_length(self):
        departamento = Departamento.objects.get(id=1)
        max_length = departamento._meta.get_field('archivo').max_length
        self.assertEquals(max_length, 100)

    # Agrega más pruebas según sea necesario para validar el comportamiento de tu modelo

    """