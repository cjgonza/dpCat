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
    autor = models.CharField(max_length = 255, verbose_name = u'Responsable')
    email = models.EmailField(verbose_name = u'Email del responsable')

    objecto_aprendizaje = models.BooleanField(default = True, verbose_name = u'Objeto de aprendizaje')

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
    informe = models.ForeignKey(InformeProduccion, editable = False)
    emisor = models.ForeignKey(User, editable = False, null = True)
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

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            str(self.fichero)
        except UnicodeEncodeError:
            raise ValidationError(u"La URI del fichero no debe contener tíldes ni caracteres especiales")

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
    KNOWLEDGE_AREAS_KEYS = (
        (u'Ciencias de la Salud',
            (
                ('AB', u'Anatomía Patológica [020]'),
                ('AC', u'Anatomía y Anatomía Patológica Comparadas [025]'),
                ('AD', u'Anatomía y Embriología Humana [027]'),
                ('FC', u'Antropología Física [028]'),
                ('CJ', u'Biología Celular [050]'),
                ('AE', u'Cirugía [090]'),
                ('AF', u'Dermatología [183]'),
                ('AG', u'Enfermería [255]'),
                ('AH', u'Estomatología [275]'),
                ('AI', u'Farmacia y Tecnología Farmacéutica [310]'),
                ('AJ', u'Farmacología [315]'),
                ('CP', u'Fisiología [410]'),
                ('AK', u'Fisioterapia [413]'),
                ('CR', u'Genética [420]'),
                ('AL', u'Histología [443]'),
                ('AM', u'Inmunología [566]'),
                ('AN', u'Medicina [610]'),
                ('AO', u'Medicina Legal y Forense [613]'),
                ('AP', u'Medicina Preventiva y Salud Pública [615]'),
                ('AQ', u'Medicina y Cirugía Animal [617]'),
                ('AR', u'Nutrición y Bromatología [640]'),
                ('AS', u'Obstetricia y Ginecología [645]'),
                ('AT', u'Oftalmología [646]'),
                ('AV', u'Otorrinolaringología [653]'),
                ('AW', u'Parasitología [660]'),
                ('AX', u'Pediatría [670]'),
                ('BY', u'Personalidad, Evaluación y Tratamiento Psicológico [680]'),
                ('AY', u'Psicobiología [725]'),
                ('AZ', u'Psiquiatría [745]'),
                ('BA', u'Radiología y Medicina Física [770]'),
                ('DB', u'Sanidad Animal [773]'),
                ('BB', u'Toxicología [807]'),
            )
        ),
        (u'Ciencias Sociales y Jurídicas',
            (
                ('FB', u'Análisis Geográfico Regional [010]'),
                ('FD', u'Antropología Social [030]'),
                ('BD', u'Biblioteconomía y Documentación [040]'),
                ('BE', u'Ciencia Política y de la Administración [070]'),
                ('BF', u'Comercialización e Investigación de Mercados [095]'),
                ('BG', u'Comunicación Audiovisual y Publicidad [105]'),
                ('BH', u'Derecho Administrativo [125]'),
                ('BI', u'Derecho Civil [130]'),
                ('BJ', u'Derecho Constitucional [135]'),
                ('BK', u'Derecho del Trabajo y de la Seguridad Social [140]'),
                ('BL', u'Derecho Eclesiástico del Estado [145]'),
                ('BM', u'Derecho Financiero y Tributario [150]'),
                ('BN', u'Derecho Internacional Privado [155]'),
                ('BO', u'Derecho Internacional Público y Relaciones Internacionales [160]'),
                ('BP', u'Derecho Mercantil [165]'),
                ('BQ', u'Derecho Penal [170]'),
                ('BR', u'Derecho Procesal [175]'),
                ('BS', u'Derecho Romano [180]'),
                ('FG', u'Didáctica de la Expresión Corporal [187]'),
                ('FH', u'Didáctica de la Expresión Musical [189]'),
                ('FI', u'Didáctica de la Expresión Musical, Plástica y Corporal (Desagregada) [190]'),
                ('FJ', u'Didáctica de la Expresión Plástica [193]'),
                ('FK', u'Didáctica de la Lengua y la Literatura [195]'),
                ('FL', u'Didáctica de la Matemática [200]'),
                ('FM', u'Didáctica de las Ciencias Experimentales [205]'),
                ('FN', u'Didáctica de las Ciencias Sociales [210]'),
                ('FO', u'Didáctica y Organización Escolar [215]'),
                ('FQ', u'Educación Física y Deportiva [245]'),
                ('BT', u'Economía Aplicada [225]'),
                ('BU', u'Economía Financiera y Contabilidad [230]'),
                ('BV', u'Economía, Sociología y Política Agraria [235]'),
                ('BW', u'Fundamentos del Análisis Económico [415]'),
                ('GK', u'Geografía Física [430]'),
                ('GL', u'Geografía Humana [435]'),
                ('HC', u'Metodología de las Ciencias del Comportamiento [620]'),
                ('HD', u'Métodos de Investigación y Diagnóstico en Educación [625]'),
                ('BX', u'Periodismo [675]'),
                ('BZ', u'Psicología Básica [730]'),
                ('CA', u'Psicología Evolutiva y de la Educación [735]'),
                ('CB', u'Psicología Social [740]'),
                ('CC', u'Sociología [775]'),
                ('HJ', u'Teoría e Historia de la Educación [805]'),
                ('CE', u'Trabajo Social y Servicios Sociales [813]'),
                ('CD', u'Urbanística y Ordenación del Territorio [815]'),
            )
        ),
        (u'Ciencias',
            (
                ('CG', u'Álgebra [005]'),
                ('CH', u'Análisis Matemático [015]'),
                ('CI', u'Astronomía y Astrofísica [038]'),
                ('CK', u'Bioquímica y Biología Molecular [060]'),
                ('CL', u'Botánica [063]'),
                ('DL', u'Cristalografía y Mineralogía [120]'),
                ('CM', u'Ecología [220]'),
                ('DM', u'Edafología y Química Agrícola [240]'),
                ('DN', u'Electromagnetismo [247]'),
                ('CN', u'Estadística e Investigación Operativa [265]'),
                ('DP', u'Estratigrafía [280]'),
                ('DT', u'Física Aplicada [385]'),
                ('DU', u'Física Atómica, Molecular y Nuclear [390]'),
                ('DV', u'Física de la Materia Condensada [395]'),
                ('DW', u'Física de la Tierra [398]'),
                ('CO', u'Física Teórica [405]'),
                ('CQ', u'Fisiología Vegetal [412]'),
                ('DX', u'Geodinámica Externa [427]'),
                ('DY', u'Geodinámica Interna [428]'),
                ('CS', u'Geometría y Topología [440]'),
                ('CT', u'Matemática Aplicada [595]'),
                ('CU', u'Microbiología [630]'),
                ('AU', u'Óptica [647]'),
                ('ES', u'Petrología y Geoquímica [685]'),
                ('CZ', u'Producción Animal [700]'),
                ('DA', u'Producción Vegetal [705]'),
                ('CV', u'Química Analítica [750]'),
                ('CW', u'Química Física [755]'),
                ('CX', u'Química Inorgánica [760]'),
                ('CY', u'Química Orgánica [765]'),
                ('DC', u'Zoología [819]'),
            )
        ),
        (u'Arquitectura e Ingeniería',
            (
                ('DE', u'Arquitectura y Tecnología de Computadores [035]'),
                ('DF', u'Ciencia de los Materiales e Ingeniería Metalúrgica [065]'),
                ('DG', u'Ciencia de la Computación e Inteligencia Artificial [075]'),
                ('DH', u'Ciencias y Técnicas de la Navegación [083]'),
                ('DI', u'Composición Arquitectónica [100]'),
                ('DJ', u'Construcciones Arquitectónicas [110]'),
                ('DK', u'Construcciones Navales [115]'),
                ('DO', u'Electrónica [250]'),
                ('DQ', u'Explotación de Minas [295]'),
                ('DR', u'Expresión Gráfica Arquitectónica [300]'),
                ('DS', u'Expresión Gráfica en la Ingeniería [305]'),
                ('DZ', u'Ingeniería Aeroespacial [495]'),
                ('EA', u'Ingeniería Agroforestal [500]'),
                ('EB', u'Ingeniería Cartográfica, Geodésica y Fotogrametría [505]'),
                ('EC', u'Ingeniería de la Construcción [510]'),
                ('ED', u'Ingeniería de los Procesos de Fabricación [515]'),
                ('EE', u'Ingeniería de Sistemas y Automática [520]'),
                ('EF', u'Ingeniería del Terreno [525]'),
                ('EG', u'Ingeniería e Infraestructura de los Transportes [530]'),
                ('EH', u'Ingeniería Eléctrica [535]'),
                ('EI', u'Ingeniería Hidráulica [540]'),
                ('EJ', u'Ingeniería Mecánica [545]'),
                ('EK', u'Ingeniería Nuclear [550]'),
                ('EL', u'Ingeniería Química [555]'),
                ('EM', u'Ingeniería Telemática [560]'),
                ('EN', u'Ingeniería Textil y Papelera [565]'),
                ('EO', u'Lenguajes y Sistemas Informáticos [570]'),
                ('EP', u'Máquinas y Motores Térmicos [590]'),
                ('EQ', u'Mecánica de Fluídos [600]'),
                ('ER', u'Mecánica de Medios Contínuos y Teoría de Estructuras [605]'),
                ('ET', u'Prospección e Investigación Minera [710]'),
                ('EU', u'Proyectos Arquitectónicos [715]'),
                ('EV', u'Proyectos de Ingeniería [720]'),
                ('EW', u'Tecnología de Alimentos [780]'),
                ('EX', u'Tecnología Electrónica [785]'),
                ('EY', u'Tecnologías del Medio Ambiente [790]'),
                ('EZ', u'Teoría de la Señal y Comunicaciones [800]'),
            )
        ),
        (u'Artes y Humanidades',
            (
                ('FE', u'Arqueología [033]'),
                ('FF', u'Ciencias y Técnicas Historiográficas [085]'),
                ('FP', u'Dibujo [185]'),
                ('FR', u'Escultura [260]'),
                ('FS', u'Estética y Teoría de las Artes [270]'),
                ('FT', u'Estudios Arabes e Islámicos [285]'),
                ('FU', u'Estudios de Asía Oriental (BOE 27/02/2003) [568]'),
                ('FV', u'Estudios Hebreos y Arameos [290]'),
                ('FW', u'Filología Alemana [320]'),
                ('FX', u'Filología Catalana [325]'),
                ('FY', u'Filología Eslava [327]'),
                ('FZ', u'Filología Francesa [335]'),
                ('GA', u'Filología Griega [340]'),
                ('GB', u'Filología Inglesa [345]'),
                ('GC', u'Filología Italiana [350]'),
                ('GD', u'Filología Latina [355]'),
                ('GE', u'Filología Románica [360]'),
                ('GF', u'Filología Vasca [365]'),
                ('GG', u'Filología Gallega y Portuguesa [370]'),
                ('GH', u'Filosofía [375]'),
                ('GI', u'Filosofía del Derecho [381]'),
                ('GJ', u'Filosofía Moral [383]'),
                ('GM', u'Historia Antigua [445]'),
                ('GN', u'Historia Contemporánea [450]'),
                ('GO', u'Historia de América [455]'),
                ('GP', u'Historia de la Ciencia [460]'),
                ('GQ', u'Historia del Arte [465]'),
                ('GR', u'Historia del Derecho y de las Instituciones [470]'),
                ('GS', u'Historia del Pensamiento y de los Movimientos Sociales [475]'),
                ('GT', u'Historia e Instituciones Económicas [480]'),
                ('GU', u'Historia Medieval [485]'),
                ('GV', u'Historia Moderna [490]'),
                ('GW', u'Lengua Española [567]'),
                ('GX', u'Lengua y Cultura del Extremo Oriente [568]'),
                ('GY', u'Lingüística General [575]'),
                ('GZ', u'Lingüística Indoeuropea [580]'),
                ('HA', u'Literatura Española [583]'),
                ('HB', u'Lógica y Filosofía de la Ciencia [585]'),
                ('HE', u'Música [635]'),
                ('HF', u'Paleontología [655]'),
                ('HG', u'Pintura [690]'),
                ('HH', u'Prehistoria [695]'),
                ('HI', u'Teoría de la Literatura y Literatura Comparada [796]'),
                ('HK', u'Traducción e Interpretación [814]'),
            )
        ),
        (u'Difusión de proyectos de investigación',
            (
                ('HM', u'Ciencias de la Salud'),
                ('HN', u'Ciencias Sociales'),
                ('HO', u'Ciencias Experimentales'),
                ('HP', u'Arquitectura e Ingeniería'),
                ('HQ', u'Humanidades'),
            )
        ),
        (u'Institucional',
            (
                ('HS', u'Centros Académicos'),
                ('HT', u'Centros Culturales'),
                ('HU', u'Vicerrectorados'),
                ('HV', u'Rectorado'),
                ('HW', u'UDV'),
            )
        ),
        ('HX', u'Divulgación'),
    )

    LICENSE_KEYS = (
        ('CR', u'Todos los derechos reservados.'),
        ('MD', u'Creative Commons: Reconocimiento - No Comercial'),
        ('SA', u'Creative Commons: Reconocimiento - No Comercial - Compartir Igual'),
        ('ND', u'Creative Commons: Reconocimiento - No Comercial - Sin Obra Derivada'),
    )

    video = models.OneToOneField(Video, editable = False)

    knowledge_areas = models.CharField(max_length = 2, choices = KNOWLEDGE_AREAS_KEYS, verbose_name = u'Clasificación Universidad')
    title = models.CharField(max_length = 255, verbose_name = u'Título completo de la producción')
    creator = models.CharField(max_length = 255, verbose_name = u'Autor/es o creador/es')
    keyword = models.CharField(max_length = 255, verbose_name = u'Palabras clave o etiquetas', help_text = u'Pude incluir tantas como quiera siempre y cuando se separen por comas.')
    description = models.TextField(verbose_name = u'Descripción breve')
    license = models.CharField(max_length = 2, choices = LICENSE_KEYS, verbose_name = u'Licencia de uso', help_text = u'Si el contenido dispone de alguna limitación de uso, incluya aquí una referencia a su licencia.')


    class Meta:
        abstract = True

class MetadataOA(Metadata):
    AUDIENCE_KEYS = (
        ('AA', u'Profesor'),
        ('AB', u'Autor'),
        ('AC', u'Alumno'),
        ('AD', u'Coordinador'),
        ('AE', u'Otro'),
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
        ('AR', u'Lingüistica'),
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

    guideline = models.CharField(max_length = 2, choices = GUIDELINE_KEYS, verbose_name = u'Área de conocimiento UNESCO')
    #knowledge_areas = models.CharField(max_length = 2, choices = KNOWLEDGE_AREAS_KEYS, verbose_name = u'Clasificación Universidad')
    #title = models.CharField(max_length = 255, verbose_name = u'Título completo de la producción')
    #creator = models.CharField(max_length = 255, verbose_name = u'Autor/es o creador/es')
    contributor = models.CharField(max_length = 255, verbose_name = u'Colaborador/es', help_text = u'Aquellas personas, entidades u organizaciones que han participado en la creación de esta producción')
    #keyword = models.CharField(max_length = 255, verbose_name = u'Palabras clave o etiquetas', help_text = u'Pude incluir tantas como quiera siempre y cuando se separen por comas.')
    #description = models.TextField(verbose_name = u'Descripción breve')
    audience = models.CharField(max_length = 2, choices = AUDIENCE_KEYS, verbose_name = u'Audiencia o público objetivo')
    typical_age_range = models.CharField(max_length = 255, verbose_name = u'Edad de la audiencia o público objetivo')
    source = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u'Identificador de obra derivada', help_text = u'Si el contenido es derivado de otra material, indique aquí la referencia al original')
    language = models.CharField(max_length = 255, verbose_name = u'Idioma', default = u'Español')
    ispartof = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u'Serie a la que pertenece')
    location = models.CharField(max_length = 255, verbose_name = u'Localización', help_text = u'Por ejemplo: el nombre de la institución, departamento, edificio, etc.')
    venue = models.CharField(max_length = 255, verbose_name = u'Lugar de celebración', help_text = u'Por ejemplo: San Cristóbal de La Laguna, Tenerife (España)', default = u'San Cristóbal de La Laguna, Tenerife (España)')
    temporal = models.TextField(null = True, blank = True, verbose_name = u'Intervalo de tiempo', help_text = u'Si en la producción intervienen diferentes actores, indique aquí el nombre y el momento en el que interviene cada uno de ellos.')
    #license = models.CharField(max_length = 2, choices = LICENSE_KEYS, verbose_name = u'Licencia de uso', help_text = u'Si el contenido dispone de alguna limitación de uso, incluya aquí una referencia a su licencia.')
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
    dificulty = models.CharField(max_length = 2, choices = DIFICULTY_KEYS, verbose_name = u'Nivel de Dificultad')
    typical_learning_time = models.CharField(max_length = 255, verbose_name = u'Tiempo estimado para la adquisición de conocimientos', help_text = u'Ejemplo: 2 horas')
    educational_language = models.CharField(max_length = 2, choices = EDUCATIONAL_LANGUAGE_KEYS, verbose_name = u'Características del lenguaje educativo')
    purpose = models.CharField(max_length = 2, choices = PURPOSE_KEYS, verbose_name = u'Objetivo del contenido')
    unesco = models.CharField(max_length = 2, choices = UNESCO_KEYS, verbose_name = u'Dominio de conocimiento')

    class Meta:
        verbose_name = u'Metadatos'
        verbose_name_plural = u'Metadatos'

    def __unicode__(self):
        return self.video.titulo

class MetadataGen(Metadata):
    contributor = models.CharField(max_length = 255, verbose_name = u'Colaborador/es', help_text = u'Aquellas personas, entidades u organizaciones que han participado en la creación de esta producción', null = True)
    language = models.CharField(max_length = 255, verbose_name = u'Idioma', default = u'Español', null = True)
    location = models.CharField(max_length = 255, verbose_name = u'Localización', help_text = u'Por ejemplo: el nombre de la institución, departamento, edificio, etc.', null = True)
    venue = models.CharField(max_length = 255, verbose_name = u'Lugar de celebración', help_text = u'Por ejemplo: San Cristóbal de La Laguna, Tenerife (España)', default = u'San Cristóbal de La Laguna, Tenerife (España)', null = True)

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

    token = models.CharField(max_length = 25, unique = True)
    instante = models.DateTimeField(auto_now_add = True)
    video = models.OneToOneField(Video)

    def __unicode__(self):
        return self.video.titulo
