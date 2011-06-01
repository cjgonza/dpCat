#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from postproduccion import utils

import os
import signal

# Create your models here.

class PlantillaFDV(models.Model):   # (Fondo-Disapositiva-Video)
    nombre = models.CharField(max_length = 50)

    fondo = models.ImageField(upload_to = 'plantillas')

    class Meta:
        verbose_name = u'Plantilla Fondo-Diapositiva-Vídeo'

    def __unicode__(self):
        return self.nombre

class TipoVideo(models.Model):
    nombre = models.CharField(max_length = 30)
    plantilla =  models.ForeignKey(PlantillaFDV)

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    ancho = models.PositiveSmallIntegerField()
    alto = models.PositiveSmallIntegerField()
    mix = models.PositiveSmallIntegerField(default = 100)

    def __unicode__(self):
        return self.nombre

class Video(models.Model):
    VIDEO_STATUS = (
        ('INC', u'Incompleto'),                  # Creado pero sin ficheros de entrada.
        ('DEF', u'Definido'),                    # Definidos los ficheros de entrada (en cola para ser procesado).
        ('PRV', u'Procesando vídeo'),            # Está siendo procesado (montaje o copia).
        ('COM', u'Completado'),                  # Procesamiento completado (en cola para generar previsualización).
        ('PRP', u'Procesando previsualización'), # Está siendo generada la previsualización.
        ('PTU', u'Pendiente del usuario'),       # A la espera de que el usuario rellene los metadatos y acepte el vídeo.
        ('PTO', u'Pendiente del operador'),      # A la espera de que el operador rellene los metadatos.
        ('ACE', u'Aceptado'),                    # Aceptado por el usuario, a la espera de que lo valide el operador.
        ('REC', u'Rechazado'),                   # Rechazado por el usuario, a la espera de que el operador tome las medidas necesarias.
        ('LIS', u'Listo'),                       # Validado por el operador, todos los procedimientos terminados.
    )

    fichero = models.CharField(max_length = 255, editable = False)
    status = models.CharField(max_length = 3, choices = VIDEO_STATUS, editable = False, default = 'INC')
    plantilla = models.ForeignKey(PlantillaFDV, null = True, blank = True)

 
    titulo = models.CharField(max_length = 255)
    autor = models.CharField(max_length = 255)
    email = models.EmailField()

    def __unicode__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        for task in self.cola_set.all():
            task.delete()
        if self.fichero:
            utils.remove_file_path(self.fichero)
        if hasattr(self, 'previsualizacion'):
            self.previsualizacion.delete()
        super(Video, self).delete(*args, **kwargs)

    def set_status(self, st):
        self.status = st
        self.save()

    class Meta:
        permissions = (
            ("video_manager", u"Puede gestionar la creación de vídeos"),
            ("video_library", u"Puede consultar la videoteca"),
        )

class InformeProduccion(models.Model):
    video = models.OneToOneField(Video, editable = False)
    operador = models.ForeignKey(User, editable = False)
    observacion = models.TextField(null = True, blank = True)
    fecha_grabacion = models.DateTimeField(auto_now_add = True)
    fecha_validacion = models.DateTimeField(null = True)
    aprobacion = models.BooleanField(default = True)

class IncidenciaProduccion(models.Model):
    WHO = (
        ('O', u'Operador'),
        ('U', u'Usuario'),
    )

    
    informe = models.ForeignKey(InformeProduccion, editable = False)
    emisor = models.CharField(max_length = 1, choices = WHO, editable = False)
    comentario = models.TextField(null = True)
    fecha =  models.DateTimeField(auto_now_add = True)
    aceptado = models.NullBooleanField()

class HistoricoCodificacion(models.Model):
    TASK_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Píldora'),
        ('PRE', u'Previsualización')
    )

    informe = models.ForeignKey(InformeProduccion, editable = False)
    tipo = models.CharField(max_length = 3, choices = TASK_TYPE)
    fecha = models.DateTimeField()
    status = models.BooleanField()

class FicheroEntrada(models.Model):
    video = models.ForeignKey(Video, editable = False)
    tipo = models.ForeignKey(TipoVideo, editable = False, null = True)
    fichero = models.CharField(max_length = 255)

    def __unicode__(self):
        if self.tipo:
            return "%s (%s)" % (self.video.titulo, self.tipo.nombre)
        return self.video.titulo

class TecData(models.Model):
    duration = models.FloatField(null = True)
    xml_data = models.TextField(null = True)
    txt_data = models.TextField(null = True)

    video = models.OneToOneField(Video)

    class Meta:
        verbose_name = u'Información técnica'
        verbose_name_plural = u'Informaciones técnicas'

    def __unicode__(self):
        return self.video.titulo

class Previsualizacion(models.Model):
    video = models.OneToOneField(Video)
    fichero = models.CharField(max_length = 255)

    def delete(self, *args, **kwargs):
        if self.fichero:
            utils.remove_file_path(self.fichero)
        super(Previsualizacion, self).delete(*args, **kwargs)

class Metadata(models.Model):
    video = models.OneToOneField(Video, editable = False)

    AUDIENCE_KEYS = (
        ('AA', u'teacher'),
        ('AB', u'author'),
        ('AC', u'learner'),
        ('AD', u'manager'),
    )

    TYPE_KEYS = (
        ('AA', u'Conferencia'),
        ('AB', u'documental'),
        ('AC', u'coloquio'),
        ('AD', u'curso'),
        ('AE', u'institucional'),
        ('AF', u'ficción'),
        ('AG', u'mesa redonda'),
        ('AH', u'exposición de trabajos'),
        ('AI', u'apertura'),
        ('AJ', u'clausura'),
        ('AK', u'conferencia inaugural'),
        ('AL', u'conferencia de clausura'),
        ('AM', u'preguntas y respuestas'),
        ('AN', u'conferencia'),
        ('AO', u'intervención'),
        ('AP', u'presentación'),
        ('AQ', u'demostración'),
        ('AR', u'entrevista'),
        ('AS', u'video promocional'),
        ('AT', u'videoconferencia'),
    )

    INTERACTIVITY_TYPE_KEYS = (
        ('AA', u'Active'),
        ('AB', u'expositive'),
        ('AC', u'mixed'),
        ('AD', u'undefined'),
    )

    LEARNING_RESOURCE_TYPE_KEYS = (
        ('AA', u'Exercise'),
        ('AB', u'index'),
        ('AC', u'experiment'),
        ('AD', u'diagram'),
        ('AE', u'narrative'),
        ('AF', u'simulation'),
        ('AG', u'slide'),
        ('AH', u'problem statement'),
        ('AI', u'figure'),
        ('AJ', u'text'),
        ('AK', u'questionnaire'),
        ('AL', u'table'),
        ('AM', u'self assessment'),
        ('AN', u'graph'),
        ('AO', u'exam'),
    )

    INTERACTIVITY_LEVEL_KEYS = (
        ('AA', u'very low'),
        ('AB', u'low'),
        ('AC', u'medium'),
        ('AD', u'high'),
        ('AE', u'very high'),
    )

    SEMANTIC_DENSITY_KEYS = (
        ('AA', u'very low'),
        ('AB', u'low'),
        ('AC', u'medium'),
        ('AD', u'high'),
        ('AE', u'very high'),
    )

    INTENTED_END_USER_ROLE_KEYS = (
        ('AA', u'Teacher'),
        ('AB', u'author'),
        ('AC', u'learner'),
        ('AD', u'manager'),
    )

    CONTEXT_KEYS = (
        ('AA', u'primary education'),
        ('AB', u'secondary education'),
        ('AC', u'higher education'),
        ('AD', u'university first cycle'),
        ('AE', u'university second cycle'),
        ('AF', u'university postgraduate'),
        ('AG', u'technical school first cycle'),
        ('AH', u'technical school second cycle'),
        ('AI', u'professional formation'),
        ('AJ', u'continuous formation'),
        ('AK', u'vocational training'),
    )

    DIFICULTY_KEYS = (
        ('AA', u'Very easy'),
        ('AB', u'easy'),
        ('AC', u'medium'),
        ('AD', u'difficult'),
        ('AE', u'very difficult'),
    )

    EDUCATIONAL_LANGUAGE_KEYS = (
        ('AA', u'expositive'),
        ('AB', u'semantic'),
        ('AC', u'lexicon'),
    )

    PURPOSE_KEYS = (
        ('AA', u'discipline'),
        ('AB', u'idea'),
        ('AC', u'prerequisite'),
        ('AD', u'educational objective'),
        ('AE', u'accessibility restrictions'),
        ('AF', u'educational level'),
        ('AG', u'skill level'),
        ('AH', u'security level'),
    )

    GUIDELINE_KEYS = (
        ('AA', u'ciencias de la saud'),
        ('AB', u'ciencias experimentales'),
        ('AC', u'ciencias jurídico-sociales'),
        ('AD', u'ciencias tecnologicas'),
        ('AE', u'humanidades'),
    )

    UNESCO_KEYS = (
        ('AA', u'Antropología'),
        ('AB', u'Artes y letras'),
        ('AC', u'Astronomía y Astrofísica'),
        ('AD', u'Ciencias Jurídicas y Derecho'),
        ('AE', u'Ciencias Agronómicas y Veterinarias'),
        ('AF', u'Ciencias de la Tecnología'),
        ('AG', u'ciencias de la Tierra y el Cosmos'),
        ('AH', u'Ciencias de la Vida'),
        ('AI', u'Ciencias Económicas'),
        ('AJ', u'Ciencias Políticas'),
        ('AK', u'Corporativo'),
        ('AL', u'Demografía'),
        ('AM', u'ética'),
        ('AN', u'filosofía'),
        ('AO', u'física'),
        ('AP', u'geografía'),
        ('AQ', u'historia'),
        ('AR', u'lingüistia'),
        ('AS', u'lógica'),
        ('AT', u'matemáticas'),
        ('AU', u'medicina y patologías humanas'),
        ('AV', u'noticias'),
        ('AW', u'pedagogía'),
        ('AX', u'psicología'),
        ('AY', u'química'),
        ('AZ', u'sociología'),
        ('BA', u'vida universitaria'),
    )

    title = models.CharField(max_length = 255, verbose_name = u'Título')
    keyword = models.CharField(max_length = 255, verbose_name = u'Claves / etiquetas')
    description = models.TextField(verbose_name = u'Descripción')
    audience = models.CharField(max_length = 2, choices = AUDIENCE_KEYS, verbose_name = u'Audiencia / Público')
    source = models.CharField(max_length = 255, null = True, verbose_name = u'Source / ID')
    language = models.CharField(max_length = 255, verbose_name = u'Idioma')
    relation = models.CharField(max_length = 255, null = True, verbose_name = u'Producción relacionada')
    ispartof = models.CharField(max_length = 255, null = True, verbose_name = u'Es parte de')
    location = models.CharField(max_length = 255, verbose_name = u'Localización')
    venue = models.CharField(max_length = 255, verbose_name = u'Lugar de celebración')
    temporal = models.TextField(null = True, verbose_name = u'Intervalo de tiempo')
    creator = models.CharField(max_length = 255, verbose_name = u'Autor o creador')
    publisher = models.CharField(max_length = 255, verbose_name = u'Editor')
    contributor = models.CharField(max_length = 255, verbose_name = u'Colaboradores')
    license = models.CharField(max_length = 255, verbose_name = u'Licencia de uso')
    rightsholder = models.CharField(max_length = 255, verbose_name = u'Responsable derechos de autor')
    date = models.DateTimeField(verbose_name = u'Fecha de grabación')
    modified = models.DateTimeField(verbose_name = u'Fecha de modificación')
    created = models.DateTimeField(verbose_name = u'Fecha de producción')
    valid = models.DateTimeField(verbose_name = u'Fecha de validación')
    extent = models.CharField(max_length = 255, verbose_name = u'Duración')
    type = models.CharField(max_length = 2, choices = TYPE_KEYS, verbose_name = u'Tipo')
    format = models.CharField(max_length = 255, verbose_name = u'Formato')
    identifier = models.CharField(max_length = 255, verbose_name = u'Identificador del recurso')
    interactivity_type = models.CharField(max_length = 2, choices = INTERACTIVITY_TYPE_KEYS)
    learning_resource_type = models.CharField(max_length = 2, choices = LEARNING_RESOURCE_TYPE_KEYS)
    interactivity_level = models.CharField(max_length = 2, choices = INTERACTIVITY_LEVEL_KEYS)
    semantic_density = models.CharField(max_length = 2, choices = SEMANTIC_DENSITY_KEYS)
    intented_end_user_role = models.CharField(max_length = 2, choices = INTENTED_END_USER_ROLE_KEYS)
    context = models.CharField(max_length = 2, choices = CONTEXT_KEYS)
    typical_age_range = models.CharField(max_length = 255)
    dificulty = models.CharField(max_length = 2, choices = DIFICULTY_KEYS)
    typical_learning_time = models.CharField(max_length = 255)
    educational_language = models.CharField(max_length = 2, choices = EDUCATIONAL_LANGUAGE_KEYS)
    purpose = models.CharField(max_length = 2, choices = PURPOSE_KEYS)
    guideline = models.CharField(max_length = 2, choices = GUIDELINE_KEYS)
    unesco = models.CharField(max_length = 2, choices = UNESCO_KEYS)

    class Meta:
        verbose_name = u'Metadatos'
        verbose_name_plural = u'Metadatos'

    def __unicode__(self):
        return self.video.titulo


## COLA ##

class ColaManager(models.Manager):
    """
    Devuelve el número de trabajos que están siendo codificados en este momento.
    """
    def count_actives(self):
        return super(ColaManager, self).get_query_set().filter(status = 'PRO').count()

    """
    Devuelve el número de trabajos que están pendientes de ser procesados
    """
    def count_pendings(self):
        return super(ColaManager, self).get_query_set().filter(status = 'PEN').count()

    """
    Devuelve la lista de vídeos pendientes de ser procesados.
    """
    def get_pendings(self):
         return super(ColaManager, self).get_query_set().filter(status = 'PEN').order_by('id')

class Cola(models.Model):
    QUEUE_STATUS = (
        ('PEN', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('HEC', 'Hecho'),
        ('ERR', 'Error'),
    )

    QUEUE_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Producción'),
        ('PRE', u'Previsualización')
    )

    objects = ColaManager()

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    tipo = models.CharField(max_length = 3, choices = QUEUE_TYPE)
    comienzo = models.DateTimeField(null = True, blank = True)
    fin = models.DateTimeField(null = True, blank = True)
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)
    pid = models.IntegerField(null = True, editable = False)

    def __unicode__(self):
       return dict(self.QUEUE_TYPE)[self.tipo] + ": " + self.video.__unicode__()

    def set_status(self, st):
        self.status = st
        self.save()

    def delete(self, *args, **kwargs):
        if self.status == 'PRO' and self.pid:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except:
                self.status = 'ERR'
                self.save()
            while Cola.objects.get(pk=self.id).status == 'PRO': pass
        super(Cola, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = u'tarea'
        verbose_name_plural = u'tareas'

class Token(models.Model):

    token = models.CharField(max_length = 25)
    instante = models.DateTimeField(auto_now_add = True)
    video = models.OneToOneField(Video)

    def __unicode__(self):
        return self.video.titulo
