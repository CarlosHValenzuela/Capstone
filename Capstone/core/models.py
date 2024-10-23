from django.db import models
from django.contrib.auth.models import User
from .choices import tipos

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    telefono = models.CharField(max_length=10)
    correo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100,choices=tipos,default='R')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Auto(models.Model):
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=100)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} {self.persona}"