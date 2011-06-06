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
    fecha_grabacion = models.DateTimeField()
    fecha_produccion = models.DateTimeField(auto_now_add = True)
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
        ('AA', u'Profesor'),
        ('AB', u'Autor'),
        ('AC', u'Alumno'),
        ('AD', u'Otro'),
    )

    TYPE_KEYS = (
        ('AA', u'Conferencia'),
        ('AB', u'Documental'),
        ('AC', u'Coloquio'),
        ('AD', u'Curso'),
        ('AE', u'Institucional'),
        ('AF', u'Ficción'),
        ('AG', u'Mesa redonda'),
        ('AH', u'Exposición de trabajos'),
        ('AI', u'Apertura'),
        ('AJ', u'Clausura'),
        ('AK', u'Conferencia inaugural'),
        ('AL', u'Conferencia de clausura'),
        ('AM', u'Preguntas y respuestas'),
        ('AN', u'Intervención'),
        ('AO', u'Presentación'),
        ('AP', u'Demostración'),
        ('AQ', u'Entrevista'),
        ('AR', u'Video promocional'),
        ('AS', u'Videoconferencia'),
    )

    INTERACTIVITY_TYPE_KEYS = (
        ('AA', u'Activa'),
        ('AB', u'Expositiva'),
        ('AC', u'Combinada (activa y expositiva)'),
        ('AD', u'Otra'),
    )

    LEARNING_RESOURCE_TYPE_KEYS = (
        ('AA', u'Ejercicio'),
        ('AB', u'Índice'),
        ('AC', u'Experimento'),
        ('AD', u'Diagrama'),
        ('AE', u'Narración'),
        ('AF', u'Simulación'),
        ('AG', u'Presentación'),
        ('AH', u'Enunciado del problema'),
        ('AI', u'Figura'),
        ('AJ', u'Texto'),
        ('AK', u'Cuestionario'),
        ('AL', u'Tabla'),
        ('AM', u'Autoevaluación'),
        ('AN', u'Gráfico'),
        ('AO', u'Examen'),
    )

    INTERACTIVITY_LEVEL_KEYS = (
        ('AA', u'Muy bajo: Documento, imagen, video, sonido, etc. de carácter expositivo.'),
        ('AB', u'Bajo: Conjunto de documentos, imágenes, vídeos, sonidos, etc. enlazados.'),
        ('AC', u'Medio: El contenido dispone de elementos interactivos'),
        ('AD', u'Alto: Cuestionario, consulta, encuesta, examen, ejercicio, etc.'),
        ('AE', u'Muy alto: Juego, simulación, etc.'),
    )

    SEMANTIC_DENSITY_KEYS = (
        ('AA', u'Muy bajo: contenido de carácter irrelevante.'),
        ('AB', u'Bajo: contiene elementos interactivos para el usuario.'),
        ('AC', u'Medio: contenido audiovisual complejo, etc.'),
        ('AD', u'Alto: gráficos, tablas, diagramas complejos, etc.'),
        ('AE', u'Muy alto: presentaciones gráficas complejas o producciones audiovisuales. '),
    )

    CONTEXT_KEYS = (
        ('AA', u'Educación primaria'),
        ('AB', u'Educación secundaria'),
        ('AC', u'Educación superior'),
        ('AD', u'Universitario de primer ciclo'),
        ('AE', u'Universitario de segundo ciclo'),
        ('AF', u'Universitario de posgrado'),
        ('AG', u'Escuela técnica de primer ciclo'),
        ('AH', u'Escuela técnica de segundo ciclo'),
        ('AI', u'Formación profesional'),
        ('AJ', u'Formación continua'),
        ('AK', u'Formación vocacional'),
    )

    DIFICULTY_KEYS = (
        ('AA', u'Muy fácil: Conocimiento, comprensión, etc.'),
        ('AB', u'Fácil: Aplicación'),
        ('AC', u'Dificultad media: Análisis'),
        ('AD', u'Difícil: Síntesis'),
        ('AE', u'Muy difícil: Evaluación'),
    )

    EDUCATIONAL_LANGUAGE_KEYS = (
        ('AA', u'Expositivo'),
        ('AB', u'Semántico'),
        ('AC', u'Lexico'),
    )

    PURPOSE_KEYS = (
        ('AA', u'Multidisciplinar'),
        ('AB', u'Descripción de concepto / idea'),
        ('AC', u'Requisito educativo'),
        ('AD', u'Mejora de competencias educativas'),
    )

    GUIDELINE_KEYS = (
        ('AA', u'Ciencias de la salud'),
        ('AB', u'Ciencias experimentales'),
        ('AC', u'Ciencias jurídico-sociales'),
        ('AD', u'Ciencias tecnológicas'),
        ('AE', u'Humanidades'),
    )

    UNESCO_KEYS = (
        ('AA', u'Antropología'),
        ('AB', u'Artes y letras'),
        ('AC', u'Astronomía y Astrofísica'),
        ('AD', u'Ciencias Jurídicas y Derecho'),
        ('AE', u'Ciencias Agronómicas y Veterinarias'),
        ('AF', u'Ciencias de la Tecnología'),
        ('AG', u'Ciencias de la Tierra y el Cosmos'),
        ('AH', u'Ciencias de la Vida'),
        ('AI', u'Ciencias Económicas'),
        ('AJ', u'Ciencias Políticas'),
        ('AK', u'Corporativo'),
        ('AL', u'Demografía'),
        ('AM', u'Ética'),
        ('AN', u'Filosofía'),
        ('AO', u'Física'),
        ('AP', u'Geografía'),
        ('AQ', u'Historia'),
        ('AR', u'Lingüistia'),
        ('AS', u'Lógica'),
        ('AT', u'Matemáticas'),
        ('AU', u'Medicina y patologías humanas'),
        ('AV', u'Noticias'),
        ('AW', u'Pedagogía'),
        ('AX', u'Psicología'),
        ('AY', u'Química'),
        ('AZ', u'Sociología'),
        ('BA', u'Vida universitaria'),
    )

    title = models.CharField(max_length = 255, verbose_name = u'Título completo de la producción')
    creator = models.CharField(max_length = 255, verbose_name = u'Autor/es o creador/es')
    contributor = models.CharField(max_length = 255, verbose_name = u'Colaborador/es', help_text = u'Aquellas personas, entidades u organizaciones que han participado en la creación de esta producción')
    keyword = models.CharField(max_length = 255, verbose_name = u'Palabras clave o etiquetas', help_text = u'Pude incluir tantas como quiera siempre y cuando se separen por comas.')
    description = models.TextField(verbose_name = u'Descripción breve')
    audience = models.CharField(max_length = 2, choices = AUDIENCE_KEYS, verbose_name = u'Audiencia o público objetivo')
    typical_age_range = models.CharField(max_length = 255, verbose_name = u'Edad de la audiencia o público objetivo')
    source = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u'Identificador de obra derivada', help_text = u'Si el contenido es derivado de otra material, indique aquí la referencia al original')
    language = models.CharField(max_length = 255, verbose_name = u'Idioma')
    ispartof = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u'Serie a la que pertenece')
    location = models.CharField(max_length = 255, verbose_name = u'Localización', help_text = u'Por ejemplo: el nombre de la institución, departamento, edificio, etc.')
    venue = models.CharField(max_length = 255, verbose_name = u'Lugar de celebración', help_text = u'Por ejemplo: San Cristóbal de La Laguna, Tenerife (España)')
    temporal = models.TextField(null = True, blank = True, verbose_name = u'Intervalo de tiempo', help_text = u'Si en la producción intervienen diferentes actores, indique aquí el nombre y el momento en el que interviene cada uno de ellos.')
    license = models.CharField(max_length = 255, verbose_name = u'Licencia de uso', help_text = u'Si el contenido dispone de alguna limitación de uso, incluya aquí una referencia a su licencia.')
    rightsholder = models.CharField(max_length = 255, verbose_name = u'Persona, entidad u organización responsable de la gestión de los derechos de autor')
    date = models.DateTimeField(verbose_name = u'Fecha de grabación', editable = False)
    created = models.DateTimeField(verbose_name = u'Fecha de producción', editable = False, help_text = u'La fecha de producción será incluida de manera automática por el sistema')
    valid = models.DateTimeField(null = True, blank = True, editable = False, verbose_name = u'Fecha de validación', help_text = u'La fecha de validación será incluida de manera automática por el sistema.')
    type = models.CharField(max_length = 2, choices = TYPE_KEYS, verbose_name = u'Tipo de producción')
    interactivity_type = models.CharField(max_length = 2, choices = INTERACTIVITY_TYPE_KEYS, verbose_name = u'Tipo de interacción con la audiencia o público objetivo')
    interactivity_level = models.CharField(max_length = 2, choices = INTERACTIVITY_LEVEL_KEYS, verbose_name = u'Nivel de interacción')
    learning_resource_type = models.CharField(max_length = 2, choices = LEARNING_RESOURCE_TYPE_KEYS, verbose_name = u'Tipo de recurso educativo')
    semantic_density = models.CharField(max_length = 2, choices = SEMANTIC_DENSITY_KEYS, verbose_name = u'Densidad semántica del contenido')
    context = models.CharField(max_length = 2, choices = CONTEXT_KEYS, verbose_name = u'Contexto educativo')
    dificulty = models.CharField(max_length = 2, choices = DIFICULTY_KEYS, verbose_name = u'Dificultad')
    typical_learning_time = models.CharField(max_length = 255, verbose_name = u'Tiempo estimado para la adquisición de conocimientos', help_text = u'Ejemplo: 2 horas')
    educational_language = models.CharField(max_length = 2, choices = EDUCATIONAL_LANGUAGE_KEYS, verbose_name = u'Características del lenguaje educativo')
    purpose = models.CharField(max_length = 2, choices = PURPOSE_KEYS, verbose_name = u'Objetivo del contenido')
    guideline = models.CharField(max_length = 2, choices = GUIDELINE_KEYS, verbose_name = u'Área de conocimiento')
    unesco = models.CharField(max_length = 2, choices = UNESCO_KEYS, verbose_name = u'Dominio de conocimiento')

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
