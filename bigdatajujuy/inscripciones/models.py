from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from tinymce.models import HTMLField
#Import Personales
from bigdatajujuy.settings import MEDIA_URL

#Creamos choices
CATEGORIA = (
        (1, 'Asistente'),
        (2, 'Expositor'),
    )

DESTINO = (
        (0, 'Solo a Mi > Prueba'),
        (1, 'Usuarios Registrados'),
        (2, 'Inscriptos'),
        (3, 'Correos Validados'),
        (4, 'Correos Sin Validar > Masivo'),
    )

# Create your models here.
class Inscripto(models.Model):
    categoria = models.IntegerField(choices=CATEGORIA, default=1)
    nombres = models.CharField('Nombres', max_length=50)
    apellido = models.CharField('Apellidos', max_length=50)
    descripcion = HTMLField('Acerca de mi', blank=True, null=True)
    foto = models.ImageField('Foto de Perfil', storage=FileSystemStorage(location=MEDIA_URL), blank=True, null=True)
    num_doc = models.CharField('Numero de Documento', max_length=50)
    telefono = models.CharField('Telefono', max_length=20)
    email = models.EmailField('Correo Electronico Personal')
    activo = models.BooleanField('Email Validado', default=False)
    autorizado = models.BooleanField('Autorizado como Expositor', default=False)
    def __str__(self):
        return(self.nombres + ' ' + self.apellido + " (" + self.get_categoria_display() + ")")

class Mails(models.Model):
    email = models.EmailField('Correo Electronico', blank=True, null=True)
    valido = models.BooleanField(default=False)
    def __str__(self):
        return(self.email)

class Mensajes(models.Model):
    nombre = models.CharField('Nombres', max_length=50)
    destinatarios = models.IntegerField(choices=DESTINO, default=0)
    cantidad = models.IntegerField(default=100)
    programar = models.DateTimeField(default=now)
    titulo = models.CharField('Titulo', max_length=50)
    cuerpo = HTMLField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    enviado = models.BooleanField(default=False)

class Progress_Links(models.Model):
    tarea = models.CharField('Tarea', max_length=50)
    inicio = models.DateTimeField(default=now)
    progress_url = models.URLField('Web', blank=True, null=True)